import os

from django.conf import settings
from django.db import models
from django.forms import FileField
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from SpellChecker.forms import DocumentForm
from SpellChecker.models import Document


def welcome(request):
    return render(request, 'welcome.html')


@login_required
def home(request):
    if request.user.is_authenticated:
        user_docs = Document.objects.get_documents_for(request.user)
        return render(request, 'files.html',
                      {'documents': user_docs})
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


@login_required
def process_file(submission: DocumentForm):
    submission.save()


@login_required
def download(request, path):
    try:
        original_document = Document.objects.get(document=path)
        all_user_docs = Document.objects.get_documents_for(request.user)
    except Document.DoesNotExist:
        raise Http404
    if original_document not in all_user_docs:
        raise HttpResponseForbidden()
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file_to_serve:
            response = HttpResponse(file_to_serve.read(), content_type='plain/txt')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
