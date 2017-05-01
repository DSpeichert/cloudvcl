from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from .osapi import os_connect
from novaclient import client as nc
from novaclient.exceptions import NotFound as NovaNotFound


class Assignment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='assignments')
    environment_definition = models.ForeignKey('EnvironmentDefinition', on_delete=models.CASCADE)

    class Meta:
        ordering = ["end_date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assignments.detail', kwargs={'pk': self.id})

    def is_current(self):
        return not (self.start_date > timezone.now() or self.end_date < timezone.now())

    is_current.boolean = True


class Course(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30)
    instructor = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        limit_choices_to={'is_instructor': True},
        related_name='instructs',
    )
    students = models.ManyToManyField('User', blank=True, related_name='studies')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses.detail', kwargs={'pk': self.id})

    def current_assignments(self):
        return self.assignments.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())


# an instance of EnvironmentDefinition that exists in OpenStack cloud
class Environment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, related_name='environments')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('environments.detail', kwargs={'pk': self.id})

    def course(self):
        return self.assignment.course


class EnvironmentDefinition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    instructor = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        limit_choices_to={'is_instructor': True},
        related_name='environment_definitions',
    )

    class Meta:
        verbose_name = "Environment Definition"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('envdefs.detail', kwargs={'pk': self.id})

    def has_instructor_free_quota_for(self, instructor, number=1):
        quota_instances = self.vmdefinition_set.count()
        quota_vcpus = 0
        quota_ram = 0
        quota_disk = 0
        for vmd in self.vmdefinition_set.all():
            quota_vcpus += vmd.flavor.vcpus
            quota_ram += vmd.flavor.ram
            quota_disk += vmd.flavor.disk

        quota_instances *= number
        quota_vcpus *= number
        quota_ram *= number
        quota_disk *= number

        return quota_instances <= instructor.free_instances() and quota_instances <= instructor.free_vcpus() and \
               quota_ram <= instructor.free_ram() and quota_disk <= instructor.free_disk()


# This is simply a reference to OpenStack Flavors. Only flavors represented by UUIDs here are available to users.
class Flavor(models.Model):
    uuid = models.CharField(max_length=36)
    name = models.TextField()
    vcpus = models.PositiveIntegerField(default=0)
    ram = models.PositiveIntegerField(default=0, verbose_name="RAM size in MB")
    swap = models.PositiveIntegerField(default=0, verbose_name="swap size in MB")
    disk = models.PositiveIntegerField(default=0, verbose_name="disk size in GB")

    class Meta:
        ordering = ['ram']

    def __str__(self):
        return self.name


class Image(models.Model):
    uuid = models.CharField(max_length=36)
    name = models.TextField()
    size = models.BigIntegerField(default=0, verbose_name="size in bytes")
    min_ram = models.PositiveIntegerField(default=0, verbose_name="min ram in MB")
    min_disk = models.PositiveIntegerField(default=0, verbose_name="min disk in GB")

    def __str__(self):
        return self.name


class User(AbstractUser):
    limit_instances = models.PositiveIntegerField(default=0, verbose_name="instance limit")
    limit_vcpus = models.PositiveIntegerField(default=0, verbose_name="vCPUs limit")
    limit_ram = models.PositiveIntegerField(default=0, verbose_name="RAM limit in MB")
    limit_disk = models.PositiveIntegerField(default=0, verbose_name="disk limit in GB")
    usage_instances = models.PositiveIntegerField(default=0, verbose_name="used instances")
    usage_vcpus = models.PositiveIntegerField(default=0, verbose_name="vCPUs usage")
    usage_ram = models.PositiveIntegerField(default=0, verbose_name="RAM usage in MB")
    usage_disk = models.PositiveIntegerField(default=0, verbose_name="disk usage in GB")
    is_instructor = models.BooleanField(
        'instructor',
        default=False,
        help_text='Designates whether this user should be treated as an instructor.'
    )
    images = models.ManyToManyField('Image', blank=True)

    def __str__(self):
        return self.get_full_name() + ' (' + self.get_username() + ')' if self.get_full_name() != '' else self.get_username()

    def free_instances(self):
        return self.limit_instances - self.usage_instances

    def free_vcpus(self):
        return self.limit_vcpus - self.usage_vcpus

    def free_ram(self):
        return self.limit_ram - self.usage_ram

    def free_disk(self):
        return self.limit_disk - self.usage_disk


# an instance of VMDefinition that exists in OpenStack cloud
class Vm(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    environment = models.ForeignKey('Environment', on_delete=models.CASCADE, related_name='vms')
    vm_definition = models.ForeignKey('VmDefinition')
    uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=10, blank=True, null=True)
    ip_address = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "VM"

    def __str__(self):
        return self.uuid

    def get_absolute_url(self):
        return reverse('environments.detail', kwargs={'pk': self.environment.id, 'uuid': self.uuid})

    def get_vnc(self):
        os_conn = os_connect()
        nova = nc.Client("2.1", session=os_conn.session)
        try:
            server = nova.servers.get(self.uuid)
            console = server.get_console_url('novnc')
            return console['console']
        except NovaNotFound:
            pass

    def claim_instructor_quota(self):
        instructor = self.environment.assignment.course.instructor
        instructor.usage_instances += 1
        instructor.usage_vcpus += self.vm_definition.flavor.vcpus
        instructor.usage_ram += self.vm_definition.flavor.ram
        instructor.usage_disk += self.vm_definition.flavor.disk
        instructor.save()

    def assignment(self):
        return self.environment.assignment

    def course(self):
        return self.environment.assignment.course

    def user(self):
        return self.environment.user


@receiver(models.signals.post_delete, sender=Vm)
def post_delete_vm(sender, instance, *args, **kwargs):
    # delete in OS
    os_conn = os_connect()
    os_conn.compute.delete_server(instance.uuid, force=True)

    # decrease instructor's usage
    instructor = instance.environment.assignment.course.instructor
    instructor.usage_instances -= 1
    instructor.usage_vcpus -= instance.vm_definition.flavor.vcpus
    instructor.usage_ram -= instance.vm_definition.flavor.ram
    instructor.usage_disk -= instance.vm_definition.flavor.disk
    instructor.save()


@receiver(models.signals.pre_delete, sender=Vm)
def pre_delete_vm(sender, instance, *args, **kwargs):
    # note the end date of IP ownership
    for ip in instance.ip_owner_history.all():
        ip.end_at = timezone.now()
        ip.save()


class VmDefinition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    environment = models.ForeignKey('EnvironmentDefinition', on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.SET_NULL, null=True, blank=False)
    flavor = models.ForeignKey('Flavor', on_delete=models.SET_NULL, null=True, blank=False)
    powershell_script = models.TextField(blank=True, null=True,
                                         help_text="(Windows only) Run a Powershell script once when the instance is created.")
    timezone = models.CharField(max_length=50, blank=True, null=True,
                                help_text="(Linux-only) Example: America/New_York")
    hostname = models.CharField(max_length=20, blank=True, null=True,
                                help_text="(Linux-only) When provided, will replace the hostname generated by default.")
    cloudinit_script = models.TextField(blank=True, null=True,
                                        help_text="Please provide a cloud-init script for Ubuntu/CentOs instance")

    bash_script = models.TextField(blank=True, null=True,
                                   help_text="Please provide a bash script for Ubuntu/CentOS instance")

    class Meta:
        verbose_name = "VM Definition"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('envdefs.detail', kwargs={'pk': self.environment.id})


class IPOwnerHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_at = models.DateTimeField(null=True)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    vm = models.ForeignKey('Vm', on_delete=models.SET_NULL, null=True, related_name='ip_owner_history')

    class Meta:
        verbose_name = "IP Owner History"

    def __str__(self):
        return str(self.id)
