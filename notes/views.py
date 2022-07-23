from django.shortcuts import render, redirect
from .forms import NoteForm
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

