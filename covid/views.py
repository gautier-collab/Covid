import os
from os import walk
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from .tasks import *
from .models import Deceased, Infected, Zone, Metric


def index(request):
  
  path=f"{settings.BASE_DIR}/static_cdn/media_root"
  new_name = f"{datetime.today().year}{str(datetime.today().month).zfill(2)}{str(datetime.today().day).zfill(2)}-{str(datetime.today().hour).zfill(2)}{str(datetime.today().minute).zfill(2)}.covid-lagebericht.docx"
  for (dirpath, dirnames, filenames) in walk(path):
    for filename in filenames:
      if "lagebericht" in filename:
        current_name = filename
        os.rename(f'{path}/{current_name}',f'{path}/{new_name}')
  
  context = {
  "deceased": Deceased.objects.all(),
  "infected": Infected.objects.all(),
  "zones": Zone.objects.all(),
  "metrics": Metric.objects.all(),
  "update": Update.objects.all().last(),
  "filename": new_name
  }

  return render(request, "covid/index.html", context)

