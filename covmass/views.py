from django.shortcuts import render
from .tasks import *

# Create your views here.

def index(request):
  return render(request, "covmass/index.html", {})
