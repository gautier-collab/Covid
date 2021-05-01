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


from django.core.files.storage import FileSystemStorage

def uploadfile_view(request):
  if request.method == 'POST':
    f = request.FILES['file']
    fs = FileSystemStorage()
    filename, ext=str(f).split('.')
    file = fs.save(str(f),f)
    fileurl = fs.url(file)
    size = fs.size(file)
    return render(request, 'covmass/uploadfile.html', {
      'fileUrl':fileurl, 
      "fileName": filename,
      "ext":ext, 
      "size": size,
    })

  else:
    return render(request, 'covmass/uploadfile.html', {})













# def download(request):
  
#   context = {
#   "deceased": Deceased.objects.all(),
#   "infected": Infected.objects.all(),
#   "zones": Zone.objects.all(),
#   "metrics": Metric.objects.all(),
#   }

#   return render(request, "covmass/index.html", context)






# def upload(request):
#   if request_method == 'POST':
#     f = request.FILES['file']
#     fs = FileSystemStorage()
#     filename, ext=str(f).split('.')
#     file = fs.save(str(f),f)
#     fileurl = fs.url(file)
#     size = fs.size(file)
#     return render(request, 'covmass/uploadfile.html', {'fileurl':fileurl, fileName:filename, "ext":ext, "size": size})
#   else:
#     return render(request, 'covmass/uploadfile.html', {})

# import os
# from django.conf import settings
# from django.http import HttpResponse, Http404

# def download(request):
#   file_path = os.path.join(settings.MEDIA_ROOT, "covmass/media/report.docx")
#   if os.path.exists("covmass/media/report.docx"):
#     with open(file_path, 'rb') as fh:
#       response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#       response['Content-Disposition'] = 'inline; filename=' + os.path.basename("covmass/media/report.docx")
#       return response
#   raise Http404