from django import forms
from .models import Professor, Student


class ProfessorRegisterForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['department', 'phone_number']


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['department', 'phone_number', 'professor']
