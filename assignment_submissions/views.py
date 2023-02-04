from django.shortcuts import render
from .models import Assignment, Submission
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .forms import SubmissionForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignment_submissions/assignments.html'
    context_object_name = 'assignments'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.professor:
            return Assignment.objects.filter(prof=user)
        else:
            return Assignment.objects.filter(prof=user.student.professor)


class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'assignment_submissions/assignment_detail.html'
    context_object_name = 'assignment'

    def get_context_data(self, **kwargs):
        if self.request.user.professor:
            return super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context['submission_form'] = SubmissionForm()
        return context


class AssignmentCreateView(CreateView):
    model = Assignment
    template_name = 'assignment_submissions/assignment_form.html'
    fields = ['name', 'description', 'test_cases']

    def form_valid(self, form):
        form.instance.prof = self.request.user
        return super().form_valid(form)


class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Assignment
    template_name = 'assignment_submissions/assignment_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        assignment = self.get_object()
        if self.request.user == assignment.prof:
            return True
        return False


class SubmissionListView(ListView):
    model = Submission
    template_name = 'assignment_submissions/submissions.html'
    context_object_name = 'submissions'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.professor:
            assignment = Assignment.objects.filter(self.request.GET.get('assignment_id'))
            return Submission.objects.filter(assignment=assignment)
        else:
            return Submission.objects.filter(student=user)


class SubmissionDetailView(DetailView):
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
    success_url = '/'

    def test_func(self):
        submission = self.get_object()
        if self.request.user == submission.student:
            return True
        return False

