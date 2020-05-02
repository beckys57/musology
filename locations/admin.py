from django.contrib import admin
from .models import City, District, Location

# Register your models here.
admin.site.register(City)
admin.site.register(District)
admin.site.register(Location)