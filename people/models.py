import random

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

class Population(models.Model):
  district = models.OneToOneField('locations.District', on_delete=models.SET_NULL, null=True, blank=True)
  size = models.PositiveSmallIntegerField(null=True, blank=True)

  class Meta:
    verbose_name_plural = "populus"

  def __str__(self):
    return "people of {}".format(self.district)

  # def respond_to(self, event):




  def initialize(self):
    if self.crowds:
      return self.crowds.all()

    # Initialize crowds
    from genres.models import Genre
    # Take all genres except one
    genres = list(Genre.objects.all())
    print("{} Genres".format(len(genres)))
    # Make one the main genre
    majority = random.choice(genres)
    maj_proportion = random.randint(40,80)
    crowds = []
    crowds.append(Crowd.objects.create(population=self, genre=majority, proportion=maj_proportion))

    remaining = 100-maj_proportion
    for genre in [g for g in genres if not g == majority][:-1]:
      if remaining > 0:
        proportion = random.randint(1, remaining)
        remaining -= proportion
        crowds.append(Crowd.objects.create(population=self, genre=genre, proportion=proportion))

    self.crowds.set(crowds)
    return self.crowds.all()

class Crowd(models.Model):
  population = models.ForeignKey(Population, on_delete=models.CASCADE, related_name="crowds")
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  proportion = models.PositiveSmallIntegerField(null=True, blank=True)

  def __str__(self):
    return "{}% {}".format(self.proportion, self.genre)

class Job(models.Model):
  JOB_ROLES = [
    ('bar staff', 'bar staff'),
    ('techie', 'techie'),
    ('roadie', 'roadie'),
    ('musician', 'musician'),
    ('promoter', 'promoter'),
    ('venue owner', 'venue owner'),
  ]
  workplace = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL)
  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  role = models.CharField(max_length=27, choices=JOB_ROLES)

  def __str__(self):
    if self.role:
      return self.role

    return "{} (unassigned to a role)".format(self.person.name)

# class Employee(models.Model):
#   class Meta:
#     abstract = True

class Musician(models.Model):
  band = models.ForeignKey('brand.Band', null=True, blank=True, on_delete=models.SET_NULL, related_name="musicians")
  person = models.ForeignKey('people.Person', on_delete=models.CASCADE, related_name="music_career")
  
  # @property
  # def show_current(self):
  #   return "Jammin' with {}".format(self.band)

#   def __str__(self):
#     if self.band:
#       return "{} ({})".format(self.person.name, self.band)

#     return "{} (not in band)".format(self.person.name)

#   class Meta:
#     verbose_name_plural = "musicians (job)"

# class BarStaff(Employee):
#   def __str__(self):
#     return "{} (Bar Staff)".format(self.person.name)

#   class Meta:
#     verbose_name_plural = "bar staff (job)"

#   def __str__(self):
#     return "{} (Bar staff at {})".format(self.person.name, self.workplace or "nowhere")

# class Techie(Employee):
#   def __str__(self):
#     return "{} (Techie at {})".format(self.person.name, self.workplace or "nowhere")

#   class Meta:
#     verbose_name_plural = "techies (job)"

# class Roadie(Employee):
#   def __str__(self):
#     return "{} (Roadie at {})".format(self.person.name, self.workplace or "nowhere")

#   class Meta:
#     verbose_name_plural = "roadies (job)"

# class Promoter(Employee):
#   def __str__(self):
#     return "{} (Promoter at {})".format(self.person.name, self.workplace or "nowhere")

#   class Meta:
#     verbose_name_plural = "promoters (job)"

# class VenueOwner(Employee):
#   def __str__(self):
#     return "{} (Venue Owner at {})".format(self.person.name, self.workplace or "nowhere")

#   class Meta:
#     verbose_name_plural = "venue owners (job)"


# All performing musicians should be in a band, even if solo artist
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

  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL)
  job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.SET_NULL)

  name = models.CharField(max_length=60)
  happiness = models.CharField(max_length=1, null=True, blank=True)
  influence = models.PositiveSmallIntegerField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "people"

  def __str__(self):
    return self.name