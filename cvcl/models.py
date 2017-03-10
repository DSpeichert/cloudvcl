from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Assignment(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    environment_definition = models.ForeignKey('EnvironmentDefinition', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# an instance of EnvironmentDefinition that exists in OpenStack cloud
class Environment(models.Model):
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class EnvironmentDefinition(models.Model):
    def __str__(self):
        return self.id


# This is simply a reference to OpenStack Flavors. Only flavors represented by UUIDs here are available to users.
class Flavor(models.Model):
    uuid = models.UUIDField()

    def __str__(self):
        return self.uuid


class Image(models.Model):
    uuid = models.UUIDField()

    def __str__(self):
        return self.uuid


class User(AbstractUser):
    limit_instances = models.IntegerField(default=0)
    limit_cpus = models.IntegerField(default=0)
    limit_ram = models.IntegerField(default=0, verbose_name="RAM limit in bytes")
    is_instructor = models.BooleanField(
        'instructor',
        default=False,
        help_text='Designates whether this user should be treated as an instructor.'
    )
    courses = models.ManyToManyField('Course')
    images = models.ManyToManyField('Image')

    def __str__(self):
        return self.username


class Course(models.Model):
    name = models.CharField(max_length=30)
    instructor = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'is_instructor': True},
                                   related_name='instructs')
    students = models.ManyToManyField('User')

    def __str__(self):
        return self.id


# an instance of VMDefinition that exists in OpenStack cloud
class Vm(models.Model):
    uuid = models.UUIDField()
    ip_address = models.GenericIPAddressField()
    environment = models.ForeignKey('Environment', on_delete=models.CASCADE)
    vm_definition = models.ForeignKey('VmDefinition')

    def __str__(self):
        return self.uuid


class VmDefinition(models.Model):
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    flavor = models.ForeignKey('Flavor', on_delete=models.CASCADE)
    user_script = models.TextField()

    def __str__(self):
        return self.id
