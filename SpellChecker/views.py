from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def welcome(request):
    return render(request, 'welcome.html')


@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'files.html')
    else:
        return redirect('welcome')
