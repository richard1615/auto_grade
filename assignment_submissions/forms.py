from django import forms
from .models import Assignment, Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code']