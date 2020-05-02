import random

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


# All musicians should be in a band, even if solo artist
class Person(models.Model):
  HAPPINESS_LEVELS = [
    ("0", "majorly foo'd off"),
    ("1", "really???"),
    ("2", "this sucks!!"),
    ("3", "meh."),
    ("4", "i mean, life's been better"),
    ("5", "taking it as it comes"),
    ("6", "pretty chill"),
    ("7", "in the vibe!"),
    ("8", "yeahhh! ROCK OONN!"),
    ("9", "cloud 9, this is nirvana, man..."),
  ]
  name = models.CharField(max_length=60)
  birthday = models.DateField()
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL)

  job_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
  job_id = models.PositiveIntegerField(null=True, blank=True)
  job_object = GenericForeignKey('job_type', 'job_id')

  happiness = models.CharField(max_length=1, null=True, blank=True)
  influence = models.PositiveSmallIntegerField(null=True, blank=True)

  class Meta:
    verbose_name_plural = "people"

  def __str__(self):
    return self.name

class Population(models.Model):
  district = models.OneToOneField('locations.District', on_delete=models.SET_NULL, null=True, blank=True)
  crowds = models.ManyToManyField('genres.Genre', through='Crowd')

  class Meta:
    verbose_name_plural = "populus"

  def __str__(self):
    return "people of {}".format(self.district)

  def initialize(self):
    # Initialize crowds
    from genres.models import Genre
    # Take all genres except one
    genres = list(Genre.objects.all())[:-1]
    # Make one the main genre
    majority = random.choice(genres)
    maj_proportion = random.randint(40,80)
    crowds = []
    crowds.append(Crowd.objects.create(population=self, genre=majority, proportion=maj_proportion))

    remaining = 100-maj_proportion
    for g in genres:
      if not g == majority and remaining > 0:
        proportion = random.randint(0, remaining)
        remaining -= proportion
        crowds.append(Crowd.objects.create(population=self, genre=g, proportion=proportion))

    self.crowds.add(crowds)

class Crowd(models.Model):
  population = models.ForeignKey(Population, on_delete=models.CASCADE)
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  proportion = models.PositiveSmallIntegerField(null=True, blank=True)

class Job(models.Model):
  person = models.ForeignKey('Person', null=True, blank=True, on_delete=models.SET_NULL)
  workplace = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL)
  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)

  class Meta:
    abstract = True

class Musician(Job):
  band = models.ForeignKey('brand.Band', null=True, blank=True, on_delete=models.SET_NULL, related_name="musicians")

  def __str__(self):
    return "{} ({})".format(self.person.name, self.band)

  class Meta:
    verbose_name_plural = "musicians (job)"

class BarStaff(Job):
  def __str__(self):
    return "{} (Bar Staff)".format(self.person.name)

  class Meta:
    verbose_name_plural = "bar staff (job)"

  def __str__(self):
    return "{} (Bar staff at {})".format(self.person.name, self.workplace or "nowhere")

class Techie(Job):
  def __str__(self):
    return "{} (Techie at {})".format(self.person.name, self.workplace or "nowhere")

  class Meta:
    verbose_name_plural = "techies (job)"

class Roadie(Job):
  def __str__(self):
    return "{} (Roadie at {})".format(self.person.name, self.workplace or "nowhere")

  class Meta:
    verbose_name_plural = "roadies (job)"

class Promoter(Job):
  def __str__(self):
    return "{} (Promoter at {})".format(self.person.name, self.workplace or "nowhere")

  class Meta:
    verbose_name_plural = "promoters (job)"

class VenueOwner(Job):
  def __str__(self):
    return "{} (Venue Owner at {})".format(self.person.name, self.workplace or "nowhere")

  class Meta:
    verbose_name_plural = "venue owners (job)"






