from django.db import models

# Create your models here.
class City(models.Model):
  name = models.CharField(max_length=128)

  class Meta:
    verbose_name_plural = "cities"

    
class District(models.Model):
  city = models.ForeignKey(City, on_delete=models.PROTECT)
  name = models.CharField(max_length=128)

class Location(models.Model):
  BUILDING_CHOICES = (
        ('venue', 'music venue'),
        ('bar', 'bar'),
        ('park', 'park'),
        ('record', 'record store'),
    )

  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  name = models.CharField(max_length=128)
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  capacity = models.PositiveSmallIntegerField(null=True, blank=True)
  building = models.CharField(max_length=6, choices=BUILDING_CHOICES)
