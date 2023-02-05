from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')
