from django.db import models

# Create your models here.
class City(models.Model):
  name = models.CharField(max_length=128)

  class Meta:
    verbose_name_plural = "cities"

  def __str__(self):
    return "City of {}".format(self.name)

  def initialize(self):
    [district.initialize() for district in self.districts.all()]

    
class District(models.Model):
  city = models.ForeignKey(City, on_delete=models.PROTECT)
  name = models.CharField(max_length=128)

  def __str__(self):
    return "{} District (City of {})".format(self.name, self.city.name)

  def initialize(self):
    self.population.initialize()

class Location(models.Model):
  BUILDING_CHOICES = (
        ('venue', 'music venue'),
        ('bar', 'bar'),
        ('park', 'park'),
        ('record', 'record store'),
        ('inst', 'musical instrument shop'),
        ('lesson', 'music lessons'),
        ('studio', 'recording studio'),
        ('promo', 'promo office'),
        ('works', 'workshop'),
    )

  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  name = models.CharField(max_length=128)
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  capacity = models.PositiveSmallIntegerField(null=True, blank=True)
  building = models.CharField(max_length=6, choices=BUILDING_CHOICES)

  def __str__(self):
    return "{} ({})".format(self.name, self.get_building_display())

  def available_actions(self):
    return [('arrange_gigs', [{"slot": 0, "band_ids": []}, {"slot": 1, "band_ids": []}])]

  def arrange_gigs(self, gigs):
    gigs = []
    for gig in gigs[0:3]:
      print(gig)




