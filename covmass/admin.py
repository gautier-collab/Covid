from django.contrib import admin
from .models import Zone, Infected, Deceased, Metric, Source

admin.site.register(Zone)
admin.site.register(Infected)
admin.site.register(Deceased)
admin.site.register(Metric)
admin.site.register(Source)
