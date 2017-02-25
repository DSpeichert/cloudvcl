from django.db import models
from django.utils import timezone

class User(models.Model)
    username = models.CharField(max_length=30)
    user_group = models.ManyToManyField(UserGroup)

    def __str__(self):
    	return self.username

class UserGroup(models.Model):
    name = models.CharField(max_length=30)
    instructor_id = models.IntegerField()
    users = models.ManyToManyField(User)

    def __str__(self):
    	return self.name

class assignment(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    def __str__(self):
    	return self.name
