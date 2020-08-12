import json
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
    # Now doing this in the game_setup function
    # [district.initialize() for district in self.districts.all()]
    return
  
  def build_display_attrs():
    city = City.objects.first()
    districts = city.districts.all()
    return {
      "name": city.name,
      "latitude": city.latitude,
      "longitude": city.longitude,
      "population": sum([d.population for d in districts]),
      "districts": [d.display_attrs for d in districts]
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
    return {
      "id": self.id,
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
    return Person.objects.filter(location__district=self)

  @property
  def crowd_counts(self):
    return {genre_id: count for genre_id, count in [c.genre_count for c in self.crowds.all()]}

  @property
  def crowds_in_size_order(self):
    return list(self.crowds.all().order_by("-proportion").values('genre_id', 'proportion'))

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
                                       'gig venue',
                                       'music bar',
                                       'local pub',
                                       'club',
                                       'record store',
                                       'musical instrument shop',
                                       'music school',
                                       'recording studio',
                                       'promo office',
                                       'workshop',
                                       'band house',
                                       'park',
                                       'empty plot',
                                      ]
                                    ]
  BUILDING_CATEGORIES = {
    'venue with stage': ['concert hall', 'music bar', 'gig venue' 'club'],
    'venue without stage': ['dive bar'],
    'pub or cafe': ['local pub', 'late night cafe'],
    'shop': ['record store', 'musical instrument shop', 'guitar shop'],
    'public place': ['park'],
    'private place': ['band house'],
    'training or work': ['music school',
                         'recording studio',
                         'promo office',
                         'workshop',],
  }
  CATEGORY_CHOICES = [(l, l) for l in BUILDING_CATEGORIES.keys()]

  name = models.CharField(max_length=31, choices=BUILDING_CHOICES)
  category = models.CharField(max_length=31, choices=CATEGORY_CHOICES)
  available_event_types = models.ManyToManyField('events.EventType', through='VenueAssessment')

  def __str__(self):
    return self.name


class Location(models.Model):
  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  district = models.ForeignKey('District', null=True, blank=True, on_delete=models.SET_NULL, related_name="locations")
  building_type = models.ForeignKey(BuildingType, on_delete=models.PROTECT)
  name = models.CharField(max_length=127)
  latitude = models.CharField(max_length=12, null=True, blank=True)
  longitude = models.CharField(max_length=12, null=True, blank=True)
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)

  slots_available = models.PositiveSmallIntegerField(default=4)
  capacity = models.PositiveSmallIntegerField(null=True, blank=True, default=100)
  popularity = models.PositiveSmallIntegerField(default=1)
  
  prestige = models.PositiveSmallIntegerField(default=3) # Cleanliness, decor, damage etc
  running_cost = models.PositiveSmallIntegerField(default=50) # Cleanliness, decor, damage etc
  entry_price = models.PositiveSmallIntegerField(default=0)

  def __str__(self):
    return "{} ({})".format(self.name, self.building_type)

  @property
  def level(self):
    popularity = self.popularity
    prestige = self.prestige
    if popularity < 3 or prestige < 1: return 0
    if popularity < 5 or prestige < 2: return 1
    if popularity < 8 or prestige < 3: return 2
    if popularity < 13 or prestige < 4: return 3
    if popularity < 21 or prestige < 5: return 4
    if popularity < 34 or prestige < 6: return 5
    if popularity < 55 or prestige < 7: return 6
    if popularity < 89 or prestige < 8: return 7
    if popularity < 144 or prestige < 9: return 8

  @property
  def display_attrs(self):
    from events.models import EventType

    attrs = {k: v for k, v in self.__dict__.items()
              if k in ["id", "brand_id", "category", "district_id", "genre_id", "latitude", "longitude", "name", "slots_available", "x", "y"]}

    features = self.features.all().values("id", "name", "path_d", "filepath", "width", "height", "has_border", "tech__effects", "filepath", "width", "height", "x", "y")

    features_with_effects = list()
    for feature in features:
      f = feature.copy()
      effects_string = feature["tech__effects"]
      if effects_string:
        f.update(tech__effects=json.dumps(eval(effects_string)))
      features_with_effects.append(f)

    attrs.update({
        "stats": {
                    "level": {"value": self.level, "label": "Level"},
                    "popularity": {"value": self.total_popularity, "label": "Popularity"},
                    "prestige": {"value": self.prestige, "label": "Prestige"},
                    "running_cost": {"value": self.running_cost, "label": "Running cost"},
                    "capacity": {"value": self.capacity, "label": "Capacity"},
                  },
        "type": self.building_type.name,
        "category": self.building_type.category,
        "features": features_with_effects,
        "update_attrs": self.update_attrs,
        "event_options": EventType.options_for_location(self),
        "staff": self.staff_data,
      })
    return attrs

  @property
  def total_popularity(self):
    from people.models import Person
    return self.popularity + sum([p.popularity for p in Person.objects.filter(job__workplace=self)])

  @property
  def staff_data(self):
    from people.models import Person
    staff = Person.objects.filter(job__workplace=self)
    staff_count = staff.values('job__role').annotate(total=Count('job__role'))
    return {
      "employees": list(staff.values('genre_id', 'location_id', 'job__role', 'name', 'happiness', 'popularity')),
      "role_counts": list(staff_count)
    }

  @property
  def update_attrs(self):
    return [["name", "string"], ["entry_price", "integer"]]
    


