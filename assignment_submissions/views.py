from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from .models import Assignment, Submission
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import BaseUser
from .send_sms import send_sms


def landing(request):
    return render(request, 'assignment_submissions/landing_page.html')


# Create your views here.
class AssignmentListView(LoginRequiredMixin, ListView):
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
        return reverse('assignments_sms', kwargs={'user_id': self.request.user.id, 'assignment_id': self.object.id})


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
            assignment = Assignment.objects.get(pk=self.kwargs.get('assignment_id'))
            return Submission.objects.filter(assignment=assignment)
        else:
            return Submission.objects.filter(student=user)


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = 'assignment_submissions/submission_detail.html'
    context_object_name = 'submission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission'] = Submission.objects.get(id=self.kwargs.get('pk'))
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
            return True
        return False

    def form_valid(self, form):
        form.instance.student = self.request.user
        form.instance.assignment = Assignment.objects.get(id=self.kwargs.get('assignment_id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('submissions_sms',
                            kwargs={'user_id': self.request.user.id, 'assignment_id': self.kwargs.get('assignment_id')})


# TODO assignment submission sms is not working try to fix it
def assignments_sms(request, user_id, assignment_id):
    user = BaseUser.objects.get(id=user_id)
    professor = user.professor
    assignment = Assignment.objects.get(id=assignment_id)
    students = professor.students.all()
    for student in students:
        send_sms(student.phone_number,
                 f'Assignment {assignment.name} has been posted. Due date is {assignment.due_date}. Please check the portal for'
                 f'more details.')
    send_sms(professor.phone_number, f'Assignment {assignment.name} has been posted')
    return redirect('assignments')


def submissions_sms(request, user_id, assignment_id):
    user = BaseUser.objects.get(id=user_id)
    student = user.student
    assignment = Assignment.objects.get(id=assignment_id)
    send_sms(student.phone_number, f'Your submission for assignment {assignment.name} has been received. Please check '
                                   f'the portal for more details.')
    return redirect('assignments')
