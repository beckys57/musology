from django.core.management import call_command
from django.db import models

class Game(models.Model):
  @property
  def player_brand(self):
    from brand.models import Brand
    return Brand.objects.get(id=1)

  @property
  def current_tech(self):
    from tech.models import Tech
    return Tech.objects.filter(brand=self.player_brand)

  def __str__(self):
    from brand.models import Brand
    return " vs ".join([b.name for b in (Brand.objects.all())])

  @property
  def all_locations(self):
    from locations.models import Location
    return Location.objects.filter(district__city__game_id=self.id)

  def initialize(self):
    from brand.models import Brand
    from locations.models import City
    from locations.views import create_basic_location_features
    print("Initializing..")
    call_command('loaddata', 'fixtures/level1.json')
    self.brands.set([Brand.objects.first()])
    self.cities.set([City.objects.first()])
    print("Tech:", self.current_tech)
    [city.initialize() for city in self.cities.all()]

    for location in self.all_locations:
      create_basic_location_features(location)

  def send_data(self):
    data_example = {
      "locations": {},
      "notifications": [
        {
          "title": "You've won worst venue of the year!",
          "body": "Oh dear.",
          "actions": [], # TODO Later....
        }
      ],
    }
