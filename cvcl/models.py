import uuid

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    name = models.CharField(max_length=30)
    instructor_id = models.IntegerField()
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Environment(models.Model):
    environment_name = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    size = models.PositiveIntegerField()
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.environment_name


class VM(models.Model):
    instance_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_name = models.CharField(max_length=30)
    ip_address = models.GenericIPAddressField()
    environments = models.ForeignKey(Environment, on_delete=models.CASCADE)

    def __str__(self):
        return self.instance_uuid


class EnvironmentDefinition(models.Model):
    disk = models.PositiveIntegerField()
    cpu = models.PositiveIntegerField()
    ram = models.PositiveIntegerField()
    assignments = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    def __str__(self):
        return self.disk


class Image(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.uuid


class VmDefinition(models.Model):
    user_script = models.TextField()
    image = models.OneToOneField(Image, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user_script


class Flavor(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vm_definition = models.OneToOneField(VmDefinition, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.uuid

