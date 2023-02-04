from django.contrib import admin
from .models import Professor, Student, BaseUser
from django.contrib.auth.admin import UserAdmin


class BaseUserAdmin(UserAdmin):
    pass


# Register your models here.
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(BaseUser, BaseUserAdmin)
