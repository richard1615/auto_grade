from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class BaseUser(AbstractUser):
    is_professor = models.BooleanField(default=True)
    is_student = models.BooleanField(default=True)


class Professor(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='professor')
    department = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='student')
    department = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.user.username
