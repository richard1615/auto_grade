from django.shortcuts import render
from .forms import ProfessorRegisterForm, StudentRegisterForm
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def register(request, user_type):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        d_form = (ProfessorRegisterForm(request.POST) if
                  user_type == 'professor' else StudentRegisterForm(request.POST))
        if form.is_valid() and d_form.is_valid():
            user = form.save()
            d_form = d_form.save(commit=False)
            d_form.user = user
            d_form.save()
    else:
        form = UserCreationForm()
        d_form = ProfessorRegisterForm() if user_type == 'professor' else StudentRegisterForm()
    context = {
        'form': form,
        'd_form': d_form,
        'user_type': user_type
    }
    return render(request, 'users/register.html', context)
