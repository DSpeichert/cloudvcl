from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from .osapi import os_connect
from novaclient import client as nc


class Assignment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    environment_definition = models.ForeignKey('EnvironmentDefinition', on_delete=models.CASCADE)

    class Meta:
        ordering = ["end_date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assignments.detail', kwargs={'pk': self.id})


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
    students = models.ManyToManyField('User', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses.detail', kwargs={'pk': self.id})


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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('envdefs.detail', kwargs={'pk': self.id})


# This is simply a reference to OpenStack Flavors. Only flavors represented by UUIDs here are available to users.
class Flavor(models.Model):
    uuid = models.CharField(max_length=36)
    name = models.TextField()

    def __str__(self):
        return self.name


class Image(models.Model):
    uuid = models.CharField(max_length=36)
    name = models.TextField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    limit_instances = models.IntegerField(default=0)
    limit_cpus = models.IntegerField(default=0)
    limit_ram = models.IntegerField(default=0, verbose_name="RAM limit in bytes")
    is_instructor = models.BooleanField(
        'instructor',
        default=False,
        help_text='Designates whether this user should be treated as an instructor.'
    )
    courses = models.ManyToManyField('Course', blank=True)
    images = models.ManyToManyField('Image', blank=True)

    def __str__(self):
        return self.username


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

    def __str__(self):
        return self.uuid

    def get_absolute_url(self):
        return reverse('environment.detail', kwargs={'pk': self.environment.id, 'uuid': self.uuid})

    def get_vnc(self):
        os_conn = os_connect()
        nova = nc.Client("2.1", session=os_conn.session)
        server = nova.servers.get(self.uuid)
        console = server.get_console_url('novnc')
        # print(console['console'])
        return console['console']


@receiver(models.signals.post_delete, sender=Vm)
def delete_file(sender, instance, *args, **kwargs):
    os_conn = os_connect()
    os_conn.compute.delete_server(instance.uuid)


class VmDefinition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    environment = models.ForeignKey('EnvironmentDefinition', on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    flavor = models.ForeignKey('Flavor', on_delete=models.CASCADE)
    user_script = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('envdefs.detail', kwargs={'pk': self.environment.id})
