from django.db import models

class Game(object):
  cities = models.OneToManyField('locations.City')

  def initialize(self):
    [city.initialize() for city in self.cities.all()]