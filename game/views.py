from django.shortcuts import render
from brand.models import Band, Brand
from genres.models import Genre
from locations.models import City, Location

# Create your views here.
def take_turn(self):
  print("Taking turn...")

def index(request):
  map_data = [City.build_display_attrs()]
  genre_data = [g.display_attrs for g in Genre.objects.all()]
  location_data = [l.display_attrs for l in Location.objects.all()]
  brand_data = [b.display_attrs for b in Brand.objects.all()]
  band_data = [b.display_attrs for b in Band.objects.all()]
  context = {"data": {
              "genres": genre_data,
              "locations": location_data,
              "bands": band_data,
              "brands": brand_data,
            }}
  return render(request, 'game/index.html', context)
