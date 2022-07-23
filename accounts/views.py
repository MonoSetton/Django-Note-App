from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from notes.models import Note


@login_required(login_url='/login')
def home(request):
    notes = Note.objects.all()
    return render(request, 'notes/home.html', {'notes': notes})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})