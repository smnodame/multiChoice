from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

def index(request):
    return render(request, 'tutorial/index.html')

def create_question(request):
    return render(request, 'tutorial/index.html')
