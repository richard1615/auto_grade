from django.contrib import admin
from .models import Professor, Student, BaseUser


# Register your models here.
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(BaseUser)
