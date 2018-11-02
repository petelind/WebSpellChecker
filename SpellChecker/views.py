from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from SpellChecker.forms import DocumentForm


def welcome(request):
    return render(request, 'welcome.html')


@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'files.html')
    else:
        return redirect('welcome')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })
