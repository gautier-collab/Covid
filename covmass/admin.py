from django.contrib import admin
from .models import Zone, Infected, Deceased, Metric

admin.site.register(Zone)
admin.site.register(Infected)
admin.site.register(Deceased)
admin.site.register(Metric)
