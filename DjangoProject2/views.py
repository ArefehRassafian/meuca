from django.shortcuts import render
from django.views import generic
from django.utils import timezone

def home(request):
    return render(request,"index.html")

