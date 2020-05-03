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

    
class District(models.Model):
  city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="districts")
  name = models.CharField(max_length=127)
  population = models.PositiveSmallIntegerField(default=100)

  def __str__(self):
    return "{} District (City of {})".format(self.name, self.city.name)

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
                                       'park',
                                       'record store',
                                       'musical instrument shop',
                                       'music lessons',
                                       'recording studio',
                                       'promo office',
                                       'workshop',
                                       'band house',
                                      ]
                                    ]

  slots = models.ForeignKey('EventSlot', null=True, blank=True, on_delete=models.SET_NULL)
  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  capacity = models.PositiveSmallIntegerField(null=True, blank=True, default=100)
  slots_available = models.PositiveSmallIntegerField(default=4)
  prestige = models.PositiveSmallIntegerField(default=3) # Cleanliness, decor, damage etc
  running_cost = models.PositiveSmallIntegerField(default=50) # Cleanliness, decor, damage etc
  building = models.CharField(max_length=27, choices=BUILDING_CHOICES)
  name = models.CharField(max_length=127)

  def __str__(self):
    return "{} ({})".format(self.name, self.get_building_display())

  def available_actions(self):
    return [('arrange_gigs', [{"slot": 0, "band_ids": []}, {"slot": 1, "band_ids": []}])]

class EventSlot(models.Model):
  # Usually 4 events can be added to a building's slots. These can be added per turn. Some events can be 
  venue = models.ForeignKey(to='locations.Location', null=True, blank=True, on_delete=models.SET_NULL)
  event = models.ForeignKey(to='brand.Event', null=True, blank=True, on_delete=models.SET_NULL)
  parties_involved = models.ManyToManyField(to='people.Person') # Covers all staff, musicians etc
  brands_involved = models.ManyToManyField(to='brand.Brand')
  bands_involved = models.ManyToManyField(to='brand.Band')







