from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# All musicians should be in a band, even if solo artist
class Person(models.Model):
  name = models.CharField(max_length=60)
  birthday = models.DateField()
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL)

  job_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
  job_id = models.PositiveIntegerField(null=True, blank=True)
  job_object = GenericForeignKey('job_type', 'job_id')

  class Meta:
    verbose_name_plural = "people"


  def __str__(self):
    return self.name

class Population(models.Model):
  district = models.ForeignKey('locations.District', on_delete=models.SET_NULL, null=True, blank=True)
  crowds = models.ManyToManyField('genres.Genre', through='Crowd')

  class Meta:
    verbose_name_plural = "populus"

class Crowd(models.Model):
  population = models.ForeignKey(Population, on_delete=models.CASCADE)
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  proportion = models.PositiveSmallIntegerField(null=True, blank=True)

class Job(models.Model):
  person = GenericRelation(Person)
  workplace = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL)
  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)

  class Meta:
    abstract = True

class Musician(Job):
  band = models.ForeignKey('brand.Band', null=True, blank=True, on_delete=models.SET_NULL)

class BarStaff(Job):
  def __str__(self):
    return "{} (Bar Staff)".format(self.person.name)

  class Meta:
    verbose_name_plural = "bar staff"

class Techie(Job):
  def __str__(self):
    return "{} (Techie)".format(self.person.name)

class Roadie(Job):
  def __str__(self):
    return "{} (Roadie)".format(self.person.name)

class Promoter(Job):
  def __str__(self):
    return "{} (Promoter)".format(self.person.name)

class VenueOwner(Job):
  def __str__(self):
    return "{} (Venue Owner)".format(self.person.name)






