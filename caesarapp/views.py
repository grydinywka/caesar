from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def diagr(request):
    return render(request, 'diagr.html', {})