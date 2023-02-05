from eval import grade
from django.shortcuts import render
from .models import Assignment, Submission
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import os
from django.urls import reverse_lazy
from users.models import BaseUser
from .send_sms import send_sms

# Create your views here.
class AssignmentListView(ListView, LoginRequiredMixin):
    model = Assignment
    template_name = 'assignment_submissions/assignments.html'
    context_object_name = 'assignments'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_professor:
            return Assignment.objects.filter(prof=user)
        else:
            return Assignment.objects.all()


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'assignment_submissions/assignment_detail.html'
    context_object_name = 'assignment'


class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    template_name = 'assignment_submissions/assignment_form.html'
    fields = ['name', 'description', 'test_cases']

    def test_func(self):
        return self.request.user.is_professor

    def form_valid(self, form):
        form.instance.prof = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('assignments_sms', kwargs={'user_id': self.request.user.id, 'assignment_id': self.object.id})


class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Assignment
    template_name = 'assignment_submissions/assignment_confirm_delete.html'
    success_url = reverse_lazy('assignments')

    def test_func(self):
        assignment = self.get_object()
        if self.request.user == assignment.prof:
            return True
        return False


class SubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = 'assignment_submissions/submissions.html'
    context_object_name = 'submissions'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_professor:
            assignment = Assignment.objects.filter(self.request.GET.get('assignment_id'))
            return Submission.objects.filter(assignment=assignment)
        else:
            return Submission.objects.filter(student=user)


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = 'assignment_submissions/submission_detail.html'
    context_object_name = 'submission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment'] = Assignment.objects.get(id=self.request.GET.get('assignment_id'))
        return context


class SubmissionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Submission
    template_name = 'assignment_submissions/submission_confirm_delete.html'
    success_url = reverse_lazy('assignments')

    def test_func(self):
        submission = self.get_object()
        if self.request.user == submission.student:
            return True
        return False


class SubmissionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Submission
    template_name = 'assignment_submissions/submission_form.html'
    fields = ['code']

    def test_func(self):
        if self.request.user.is_student:
            return False
        return True

    def check_submission(id, extension, dir, timelimit):
        # example: id = "p1", extension = "cpp", dir = "p1", timelimit = 1
        os.chdir('assignment_submissions/eval')
        os.system(f'mkdir {id} {id}/{id}-input {id}/{id}-output')
        os.system(f'cp ../../test_cases/{id}-input*.* {id}/{id}-input/')
        os.system(f'cp ../../test_cases/{id}-output*.* {id}/{id}-output/')
        os.system(f'cp ../../code/{id}-main.cpp {id}/')

        grade.run_container(id, extension, dir, timelimit)
        res = grade.return_result()

        os.system(f'sudo rm -rf {id}/')
        # os.system(f'rm -rf {id}')
        return res

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('submissions_sms', kwargs={'user_id': self.request.user.id, 'assignment_id': self.object.id})


def assignments_sms(request, user_id, assignment_id):
    professor = BaseUser.objects.get(id=user_id)
    assignment = Assignment.objects.get(id=assignment_id)
    students = professor.students.all()
    for student in students:
        send_sms(student.phone_number, f'Assignment {assignment.name} has been posted. Please check the portal for '
                                       f'more details.')
    send_sms(professor.phone_number, f'Assignment {assignment.name} has been posted')
    return reverse_lazy('assignments')


def submissions_sms(request, user_id, assignment_id):
    student = BaseUser.objects.get(id=user_id)
    assignment = Assignment.objects.get(id=assignment_id)
    send_sms(student.phone_number, f'Your submission for assignment {assignment.name} has been received. Please check '
                                   f'the portal for more details.')
    return reverse_lazy('assignments')
