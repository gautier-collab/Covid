from django.contrib import admin
from .models import Zone, Infected, Deceased, Source, Update, Metric

class InfectedAdmin(admin.ModelAdmin):
  readonly_fields = ('update',)

admin.site.register(Update)
admin.site.register(Zone)
admin.site.register(Infected, InfectedAdmin)
admin.site.register(Deceased)
admin.site.register(Source)
