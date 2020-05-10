import random

from django.db import models
from django.db.models import Count

class City(models.Model):
  game = models.ForeignKey(to='game.Game', null=True, blank=True, on_delete=models.SET_NULL, related_name="cities")
  name = models.CharField(max_length=127)
  latitude = models.CharField(max_length=12, null=True, blank=True)
  longitude = models.CharField(max_length=12, null=True, blank=True)

  class Meta:
    verbose_name_plural = "cities"

  def __str__(self):
    return "City of {}".format(self.name)

  def initialize(self):
    [district.initialize() for district in self.districts.all()]
  
  def build_display_attrs():
    city = City.objects.first()
    return {
      "name": city.name,
      "latitude": city.latitude,
      "longitude": city.longitude,
      "districts": [d.display_attrs for d in city.districts.all()]
    }
    
class District(models.Model):
  city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="districts")
  name = models.CharField(max_length=127)
  population = models.PositiveSmallIntegerField(default=100)
  latitude = models.CharField(max_length=12, null=True, blank=True)
  longitude = models.CharField(max_length=12, null=True, blank=True)

  class Meta:
    ordering = ['id']

  def __str__(self):
    return "{} District (City of {})".format(self.name, self.city.name)

  @property
  def display_attrs(self):
    return {
      "id": self.id,
      "latitude": self.latitude,
      "longitude": self.longitude,
      "name": self.name,
      "population": self.population,
      "crowds": [c.display_attrs for c in self.crowds.all()]
      }

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

class VenueAssessment(models.Model):
  SUITABILITY_RATINGS = {
    0: 'highly inappropriate',
    1: 'very inappropriate',
    2: 'inappropriate',
    3: 'random!',
    4: 'a bit odd',
    5: 'fair',
    6: 'fine',
    7: 'apt',
    8: 'very apt',
    9: 'a perfect fit',
  }
  building_type = models.ForeignKey('BuildingType', on_delete=models.CASCADE)
  event_type = models.ForeignKey('events.EventType', on_delete=models.CASCADE)
  suitability = models.PositiveSmallIntegerField()

  def __str__(self):
    return "{} - {} at {}".format(self.suitability, self.event_type, self.building_type)

  def calculate(location, event):
    building_type = location.building_type
    event_type = event.event_type
    va = VenueAssessment.objects.filter(building_type=building_type, event_type=event_type)
    if va:
      return int(va.first().suitability)
    else:
      return -1
    
# Only of these should exist, as buildings become available. This is more of a building type
class BuildingType(models.Model):
  # When adding to BUILDING_CHOICES please also put the building in BUILDING_CATEGORIES
  BUILDING_CHOICES = [(n, n) for n in ['concert hall',
                                       'music bar',
                                       'local pub',
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
  BUILDING_CATEGORIES = {
    'venue with stage': ['concert hall', 'music bar'],
    'pub or cafe': ['local pub', 'club'],
    'shop': ['record store', 'musical instrument shop'],
    'public place': ['park'],
    'private place': ['band house'],
    'training or work': ['music lessons',
                         'recording studio',
                         'promo office',
                         'workshop',],
  }
  CATEGORY_CHOICES = [(l, l) for l in BUILDING_CATEGORIES.keys()]

  name = models.CharField(max_length=31, choices=BUILDING_CHOICES)
  category = models.CharField(max_length=31, choices=CATEGORY_CHOICES)
  available_event_types = models.ManyToManyField('events.EventType', through='VenueAssessment')

  def __str__(self):
    return "{} (building type)".format(self.name)

class Location(models.Model):
  POSTCODE_CHOICES = [(p, p) for p in [
                                        'A1', 'A2', 'A3', 'A4', 
                                        'B1', 'B2', 'B3', 'B4', 
                                        'C1', 'C2', 'C3', 'C4', 
                                        'D1', 'D2', 'D3', 'D4', 
                                      ]]

  slots = models.ForeignKey('events.EventSlot', null=True, blank=True, on_delete=models.SET_NULL)
  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  building_type = models.ForeignKey(BuildingType, on_delete=models.PROTECT)
  capacity = models.PositiveSmallIntegerField(null=True, blank=True, default=100)
  slots_available = models.PositiveSmallIntegerField(default=4)
  prestige = models.PositiveSmallIntegerField(default=3) # Cleanliness, decor, damage etc
  running_cost = models.PositiveSmallIntegerField(default=50) # Cleanliness, decor, damage etc
  name = models.CharField(max_length=127)
  postcode = models.CharField(max_length=2, default='D4', choices=POSTCODE_CHOICES)
  latitude = models.CharField(max_length=12, null=True, blank=True)
  longitude = models.CharField(max_length=12, null=True, blank=True)

  def __str__(self):
    return "{} ({})".format(self.name, self.building_type)

  @property
  def display_attrs(self):
    from events.models import EventType

    attrs = {k: v for k, v in self.__dict__.items()
              if k in ["id", "brand_id", "genre_id", "latitude", "longitude", "name", "postcode", "slots_available"]}
    stats = {
      "prestige": {"value": self.prestige, "label": "Prestige"},
      "running_cost": {"value": self.running_cost, "label": "Running cost"},
      "capacity": {"value": self.capacity, "label": "Capacity"},
    }
    attrs['stats'] = stats
    attrs['type'] = self.building_type.name
    attrs["event_options"] = EventType.options_for_location(self)
    attrs["staff"] = self.staff_data
    attrs["events"] = [{
            "slot": i,
            "kind": "",
            "band_ids": [],
            "promoter_ids": [],
            "people_ids": [],
          } for i in range(1, self.slots_available+1)]
    return attrs

  @property
  def staff_data(self):
    from people.models import Person
    staff = Person.objects.filter(job__workplace=self)
    staff_count = staff.values('job__role').annotate(total=Count('job__role'))
    return {
      "employees": list(staff.values('genre_id', 'location_id', 'job__role', 'name', 'happiness', 'influence')),
      "role_counts": list(staff_count)
    }


