from django.shortcuts import render
from brand.models import Brand
from locations.models import Location

# Create your views here.
def take_turn(self):
  print("Taking turn...")

def index(request):
  location_data = [l.display_attrs for l in Location.objects.all()]
  brand_data = [b.display_attrs for b in Brand.objects.all()]
  context = {"data": {"locations": location_data, "brands": brand_data}}
  return render(request, 'game/index.html', context)
