from django.contrib import admin
from .models import Zone, Infected, Deceased, Source, Update, Metric

# class InfectedInline(admin.TabularInline):
#   model = Infected

# class MetricAdmin(admin.ModelAdmin):
#   readonly_fields = ('update',)
#   inlines = [
#     InfectedInline,
#   ]

admin.site.register(Update)
admin.site.register(Zone)
admin.site.register(Infected)
admin.site.register(Deceased)
admin.site.register(Source)
# admin.site.register(Metrick, MetricAdmin)
