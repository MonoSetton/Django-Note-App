from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from notes.models import Note
from .decorators import unauthenticated_user


@login_required(login_url='/login')
def home(request):
    notes = Note.objects.filter(author=request.user)
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        note = Note.objects.filter(id=note_id).first()
        if note and note.author == request.user:
            note.delete()

    return render(request, 'notes/home.html', {'notes': notes})


@unauthenticated_user
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})