from django.shortcuts import render
from .tasks import *
from .models import Deceased, Infected, Zone, Metric


def index(request):
  
  context = {
  "deceased": Deceased.objects.all(),
  "infected": Infected.objects.all(),
  "zones": Zone.objects.all(),
  "metrics": Metric.objects.all(),
  }

  return render(request, "covmass/index.html", context)


# from django.core.files.storage import FileSystemStorage

# def uploadfile_view(request):
#   if request.method == 'POST':
#     f = request.FILES['file']
#     fs = FileSystemStorage()
#     filename, ext=str(f).split('.')
#     file = fs.save(str(f),f)
#     fileurl = fs.url(file)
#     size = fs.size(file)
#     return render(request, 'covmass/uploadfile.html', {
#       'fileUrl':fileurl, 
#       "fileName": filename,
#       "ext":ext, 
#       "size": size,
#     })
#   else:
#     return render(request, 'covmass/uploadfile.html', {})
