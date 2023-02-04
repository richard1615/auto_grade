from django.contrib import admin
from .models import Assignment, Submission
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Assignment)
admin.site.register(Submission)
