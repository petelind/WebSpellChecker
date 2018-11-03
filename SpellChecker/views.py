from django.forms import FileField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from SpellChecker.forms import DocumentForm
from SpellChecker.models import Document


def welcome(request):
    user_docs = Document.objects.get
    return render(request, 'welcome.html')


@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'files.html')
    else:
        return redirect('welcome')


@login_required
def model_form_upload(request):
    if request.method == 'POST':
        document = Document(user=request.user)
        form = DocumentForm(instance=document, data=request.POST, files=request.FILES)
        if form.is_valid():
            process_file(form)
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form,
    })


def process_file(submission: DocumentForm):
    submission.save()
