from django.contrib import admin

from .models import Band, RecordLabel, Event

# Register your models here.
admin.site.register(Band)
admin.site.register(RecordLabel)
admin.site.register(Event)