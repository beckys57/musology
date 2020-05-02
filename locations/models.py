from django.db import models

# Create your models here.
class City(models.Model):
  name = models.CharField(max_length=127)

  class Meta:
    verbose_name_plural = "cities"

  def __str__(self):
    return "City of {}".format(self.name)

  def initialize(self):
    [district.initialize() for district in self.districts.all()]

    
class District(models.Model):
  city = models.ForeignKey(City, on_delete=models.PROTECT)
  name = models.CharField(max_length=127)

  def __str__(self):
    return "{} District (City of {})".format(self.name, self.city.name)

  def initialize(self):
    self.population.initialize()

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
  capacity = models.PositiveSmallIntegerField(null=True, blank=True)
  slots_available = models.PositiveSmallIntegerField(default=4)
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







