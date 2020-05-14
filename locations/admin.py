from django.contrib import admin
from .models import City, District, Location, BuildingType, VenueAssessment

# Register your models here.
admin.site.register(City)
admin.site.register(District)
admin.site.register(Location)
admin.site.register(BuildingType)
admin.site.register(VenueAssessment)
