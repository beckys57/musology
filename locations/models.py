import random

from django.db import models

class City(models.Model):
  game = models.ForeignKey(to='game.Game', null=True, blank=True, on_delete=models.SET_NULL, related_name="cities")
  name = models.CharField(max_length=127)

  class Meta:
    verbose_name_plural = "cities"

  def __str__(self):
    return "City of {}".format(self.name)

  def initialize(self):
    [district.initialize() for district in self.districts.all()]
  
  def build_display_attrs():
    city = City.objects.first()
    return {
      "city": city.name,
      "districts": [d.display_attrs for d in city.districts.all()]
    }
    
class District(models.Model):
  city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="districts")
  name = models.CharField(max_length=127)
  population = models.PositiveSmallIntegerField(default=100)

  class Meta:
    ordering = ['id']

  def __str__(self):
    return "{} District (City of {})".format(self.name, self.city.name)

  @property
  def display_attrs(self):
    return {"id": self.id, "name": self.name, "population": self.population, "crowds": [c.display_attrs for c in self.crowds.all()]}

  # Generate some music-loving crowds
  def initialize(self):
    if self.crowds.first():
      return self.crowds.all()

    # Initialize crowds
    from genres.models import Genre
    from people.models import Crowd
    # Take all genres except one
    genres = list(Genre.objects.all())
    # Make one the main genre
    majority = random.choice(genres)
    maj_proportion = random.randint(40,80)
    crowds = []
    crowds.append(Crowd.objects.create(district=self, genre=majority, proportion=maj_proportion))

    remaining = 100-maj_proportion
    for genre in [g for g in genres if not g == majority][:-1]:
      if remaining > 0:
        proportion = random.randint(1, remaining)
        remaining -= proportion
        crowds.append(Crowd.objects.create(district=self, genre=genre, proportion=proportion))

    self.crowds.set(crowds)
    print(self.crowds.all())
    return self.crowds.all()

  @property
  def people(self):
    Person.objects.filter(location__district=self)

class Location(models.Model):
  BUILDING_CHOICES = [(n, n) for n in ['music venue',
                                       'bar',
                                       'club',
                                       'record store',
                                       'musical instrument shop',
                                       'music lessons',
                                       'recording studio',
                                       'promo office',
                                       'workshop',
                                       'band house',
                                       'park',
                                       'empty plot',
                                      ]
                                    ]

  POSTCODE_CHOICES = [(p, p) for p in [
                                        'A1', 'A2', 'A3', 'A4', 
                                        'B1', 'B2', 'B3', 'B4', 
                                        'C1', 'C2', 'C3', 'C4', 
                                        'D1', 'D2', 'D3', 'D4', 
                                      ]]

  slots = models.ForeignKey('events.EventSlot', null=True, blank=True, on_delete=models.SET_NULL)
  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  capacity = models.PositiveSmallIntegerField(null=True, blank=True, default=100)
  slots_available = models.PositiveSmallIntegerField(default=4)
  prestige = models.PositiveSmallIntegerField(default=3) # Cleanliness, decor, damage etc
  running_cost = models.PositiveSmallIntegerField(default=50) # Cleanliness, decor, damage etc
  building = models.CharField(max_length=27, choices=BUILDING_CHOICES)
  name = models.CharField(max_length=127)
  postcode = models.CharField(max_length=2, default='D4', choices=POSTCODE_CHOICES)

  def __str__(self):
    return "{} ({})".format(self.name, self.get_building_display())

  # @property
  # def available_actions(self):
  #   return [('events_gig', [{"slot": 0, "band_ids": []}, {"slot": 1, "band_ids": []}])]

  @property
  def display_attrs(self):
    attrs = {k: v for k, v in self.__dict__.items()
              if k in ["id", "brand_id", "capacity", "prestige", "running_cost", "name", "postcode", "slots_available"]}
    attrs['type'] = self.get_building_display()
    return attrs

  # def construct_data(self):
  #   return {
  #     "attributes": self.display_attrs(),
  #   }






