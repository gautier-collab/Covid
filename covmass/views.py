from django.shortcuts import render
from .tasks import *
from .models import Deceased, Infected, Zone, Metric

# Create your views here.

def index(request):
  
  context = {
    "deceased": Deceased.objects.all(),
    "infected": Infected.objects.all(),
    "zones": Zone.objects.all(),
    "metrics": Metric.objects.all(),
  }
  
  return render(request, "covmass/index.html", context)
