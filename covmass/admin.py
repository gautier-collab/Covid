from django.contrib import admin
from .models import Zone, Infected, Deceased, Source, Update

admin.site.register(Update)
admin.site.register(Zone)
admin.site.register(Infected)
admin.site.register(Deceased)
admin.site.register(Source)
