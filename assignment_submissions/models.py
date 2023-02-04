from django.db import models
from users.models import BaseUser
from django.utils import timezone


# Create your models here.

class Assignment(models.Model):
    name = models.CharField(max_length=100)
    prof = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='assignments')
    description = models.TextField()
    test_cases = models.FileField(upload_to='test_cases/')
    due_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,
                                   related_name='submissions')
    student = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    code = models.FileField(upload_to='code/')
    score = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.assignment.name} - {self.student.username}'
