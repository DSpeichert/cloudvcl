from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.db import transaction
from django.db.models import Q
from passlib.hash import sha512_crypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import base64
import yaml
from ..models import *
from ..forms import AssignmentForm
from ..osapi import get_default_network_id, os_connect


def is_instructor_check(user):
    return user.is_authenticated and user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class AssignmentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = './assignment_create.html'
    form_class = AssignmentForm
    success_message = "%(name)s was created successfully"

    def get_form_kwargs(self):
        kwargs = super(AssignmentCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super(AssignmentCreate, self).form_valid(form)


class AssignmentDetail(LoginRequiredMixin, DetailView):
    template_name = './assignment_detail.html'

    def get_queryset(self):
        return Assignment.objects.filter(Q(course__in=self.request.user.instructs.all()) | Q(
            course__in=self.request.user.studies.all(), start_date__lte=timezone.now(),
            end_date__gte=timezone.now())).distinct()

    def get_context_data(self, **kwargs):
        context = super(AssignmentDetail, self).get_context_data(**kwargs)
        try:
            context['environment'] = self.object.environments.get(user=self.request.user)
        except Environment.DoesNotExist:
            pass
        return context


class AssignmentList(LoginRequiredMixin, ListView):
    template_name = './assignment_list.html'

    def get_queryset(self):
        return Assignment.objects.filter(Q(course__in=self.request.user.instructs.all()) | Q(
            course__in=self.request.user.studies.all(), start_date__lte=timezone.now(),
            end_date__gte=timezone.now())).distinct()


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class AssignmentUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = './assignment_update.html'
    form_class = AssignmentForm
    success_message = "%(name)s was updated successfully"

    def get_form_kwargs(self):
        kwargs = super(AssignmentUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Assignment.objects.filter(course__in=self.request.user.instructs.all())


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class AssignmentDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = './assignment_delete.html'
    success_url = reverse_lazy('assignments')
    success_message = "%(name)s was deleted successfully"

    def get_queryset(self):
        return Assignment.objects.filter(course__in=self.request.user.instructs.all())


@method_decorator(transaction.atomic, name='dispatch')
class AssignmentLaunch(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        assignment = get_object_or_404(Assignment, pk=kwargs['pk'])
        if assignment.course.instructor != request.user:
            if assignment.start_date > timezone.now() or assignment.end_date < timezone.now():
                # student's can't launch environment outside specified dates
                messages.error(request, 'This assignment is not active.')
                return redirect("assignments.list")

        if request.user not in assignment.course.students.all():
            # student not in course/assignment
            messages.error(request, 'You are not in this course!')
            return redirect("assignments.list")

        if assignment.environments.filter(user=request.user):
            # already exists
            messages.error(request, 'You already have an environment for this assignment.')
            return redirect(assignment)

        # Check for empty environment
        if not assignment.environment_definition.vmdefinition_set.count():
            messages.error(request, "This assignment has empty environment. It doesn't make sense to launch it." +
                           "Contact your instructor.")
            return redirect(assignment)

        # Check quotas
        if not assignment.environment_definition.has_instructor_free_quota_for(assignment.course.instructor):
            messages.error(request, "Your instructor ran out of quota. Contact your instructor.")
            return redirect(assignment)

        # Save environment to DB
        environment = Environment(assignment=assignment, user=request.user)
        environment.save()

        # Check if VM definitions have image and flavors
        # It's possible that previously configured image/flavor was deleted when it was removed from OpenStack
        for vmd in environment.assignment.environment_definition.vmdefinition_set.all():
            if vmd.image is None:
                messages.error(request, 'One of VM Definitions is missing an image. Ask your instructor to fix this.')
                return redirect(assignment)

            if vmd.flavor is None:
                messages.error(request, 'One of VM Definitions is missing a flavor. Ask your instructor to fix this.')
                return redirect(assignment)

        # Create VMs
        for vmd in environment.assignment.environment_definition.vmdefinition_set.all():
            os_conn = os_connect()
            username = None
            password = None
            data_dict = {
                'users': [],
            }

            if vmd.default_user_password or vmd.default_user_public_key:
                data_dict['users'].append('default')

            if vmd.install_packages:
                packages = []
                for line in vmd.install_packages.splitlines():
                    packages.append(line.strip())
                data_dict['packages'] = packages

            if vmd.package_update is not None:
                data_dict['package_update'] = vmd.package_update

            if vmd.package_upgrade is not None:
                data_dict['package_upgrade'] = vmd.package_upgrade

            if vmd.package_reboot_if_required is not None:
                data_dict['package_reboot_if_required'] = vmd.package_reboot_if_required

            if vmd.timezone:
                data_dict['timezone'] = vmd.timezone

            if vmd.hostname:
                data_dict['hostname'] = vmd.hostname

            if vmd.default_user_password:
                data_dict['password'] = vmd.default_user_password

            if vmd.default_user_public_key:
                data_dict['ssh_authorized_keys'] = [vmd.default_user_public_key]

            if vmd.student_user:
                username = self.request.user.username
                password = get_random_string(length=8)
                data_dict['users'].append({
                    'name': username,
                    'sudo': vmd.student_user_sudo,
                    'lock_passwd': False,
                    'passwd': sha512_crypt.encrypt(password),
                })

            # put together a MIME multipart message
            user_data = MIMEMultipart()
            # when in MIME Multipart encoding, the #cloud-init shebang is not required but we provide it
            cloud_config_content = '#cloud-config\n' + yaml.dump(data_dict, default_flow_style=False)
            cloud_config_part = MIMEText(cloud_config_content, 'cloud-config', sys.getdefaultencoding())
            user_data.attach(cloud_config_part)

            if vmd.shell_script:
                shell_part = MIMEText(vmd.shell_script, 'x-shellscript', sys.getdefaultencoding())
                user_data.attach(shell_part)

            server = os_conn.compute.create_server(
                name=vmd.name + '.' + username,
                image_id=vmd.image.uuid,
                flavor_id=vmd.flavor.uuid,
                networks=[{"uuid": get_default_network_id()}],
                user_data=base64.b64encode(user_data.as_string().encode('utf-8')).decode('utf-8')
            )

            vm = environment.vms.create(
                name=server.name,
                uuid=server.id,
                status=server.status,
                ip_address=server.access_ipv4,
                vm_definition=vmd,
                username=username,
                password=password,
            )
            vm.save()
            vm.claim_instructor_quota()

            server = os_conn.compute.wait_for_server(server)
            server = os_conn.compute.get_server(server.id)
            vm.status = server.status
            vm.ip_address = server.addresses[list(server.addresses.keys())[0]][0]['addr']
            vm.save()

            ip_owner_history = vm.ip_owner_history.create(
                ip_address=vm.ip_address,
                user=request.user
            )
            ip_owner_history.save()

        return redirect(environment)
