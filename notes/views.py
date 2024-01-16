from django.shortcuts import render, redirect
from .forms import NoteForm
from .models import Note
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('/home')
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})


@login_required(login_url='/login')
def update_note(request, pk):
    note = Note.objects.get(id=pk)
    form = NoteForm(instance=note)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note.save()
            return redirect('/home')
    return render(request, 'notes/update_note.html', {'form': form})


def delete_note(request, pk):
    note = Note.objects.get(id=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('/home')
    return render(request, 'notes/delete_note.html', {'note': note})

