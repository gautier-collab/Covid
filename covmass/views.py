from django.shortcuts import render
from .task import *

# Create your views here.

def index(request):
  sleepy(2)
  return render(request, "covmass/index.html", {})
