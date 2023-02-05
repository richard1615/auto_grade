from django.shortcuts import render, redirect
from .forms import ProfessorRegisterForm, StudentRegisterForm, SignUpForm


# Create your views here.
def register(request, user_type):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        d_form = (ProfessorRegisterForm(request.POST) if
                  user_type == 'professor' else StudentRegisterForm(request.POST))
        if form.is_valid() and d_form.is_valid():
            user = form.save(commit=False)
            user.is_professor = True if user_type == 'professor' else False
            user.is_student = True if user_type == 'student' else False
            user.save()
            d_form = d_form.save(commit=False)
            d_form.user = user
            d_form.save()
            return redirect('login')
    else:
        form = SignUpForm()
        d_form = ProfessorRegisterForm() if user_type == 'professor' else StudentRegisterForm()
    context = {
        'form': form,
        'd_form': d_form,
        'user_type': user_type
    }
    return render(request, 'users/register.html', context)
