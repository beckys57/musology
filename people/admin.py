from django.contrib import admin
from .models import Person, Population, Crowd, Musician, BarStaff, Techie, Roadie, Promoter, VenueOwner

# Register your models here.
admin.site.register(Person)
admin.site.register(Population)
admin.site.register(Crowd)
admin.site.register(Musician)
admin.site.register(BarStaff)
admin.site.register(Techie)
admin.site.register(Roadie)
admin.site.register(Promoter)
admin.site.register(VenueOwner)