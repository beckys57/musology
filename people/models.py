import math
import random

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator

class Crowd(models.Model):
  district = models.ForeignKey('locations.District', null=True, on_delete=models.CASCADE, related_name="crowds")
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  proportion = models.PositiveSmallIntegerField(null=True, blank=True)

  def __str__(self):
    return "{}% {}".format(self.proportion, self.genre)

  @property
  def display_attrs(self):
    return {"genre_id": self.genre.id, "colour": self.genre.colour, "proportion": self.proportion}

  @property
  def genre_count(self):
    return [self.genre.id, math.floor(self.proportion*self.district.population/100)]

class Job(models.Model):
  JOB_ROLES = [(r, r) for r in [
      'bar staff',
      'techie',
      'roadie',
      'musician',
      'teacher', # Teaches skill based on where employed
      'promoter',
      'venue owner',
    ]
  ]
  workplace = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL)
  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  role = models.CharField(max_length=27, choices=JOB_ROLES)

  @property
  def person(self):
    return self.employees.first()
  
  class Meta:
    verbose_name = 'Cool cat'
    verbose_name_plural = 'People in the industry'

  def __str__(self):
    return "{} (job)".format(self.role)

class Musician(models.Model):
  band = models.ForeignKey('brand.Band', null=True, blank=True, on_delete=models.SET_NULL, related_name="musicians")
  person = models.ForeignKey('people.Person', on_delete=models.CASCADE, related_name="music_career")
  
  def __str__(self):
    return "{} (Musician in {})".format(self.person, self.band)

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

def HAIR_COLORS():
  return random.choice(["#000000", "#c7ff92", "#98816a", "#38250c", "#f0e8fb", "#ff9752", "#3bb3ab", "#1e2629", "#d6abc8", "#e8fbf8", "#947d31", "#594527", "#495919", "#94682a"])

def SKIN_COLORS():
  return random.choice(["#ffc999", "#754b32", "#feebe5", "#f5e1c8", "#d7ad93", "#412d29"])

def CLOTHING_COLORS():
  return random.choice(["#000000", "#280c38", "#32380c", "#38250c", "#6a6b98", "#98816a", "#98986a", "#976a98", "#7393d8", "#d8b673", "#d88473", "#b72f36", "#2fb7a9", "#7ab72f", "#e8fbf8", "#fbece8", "#fbf6e8", "#f0e8fb", ])

def HAIR_STYLES():
  return str(random.choice([i for i in range(6)])+1)

def SHIRT_STYLES():
  return str(random.choice([i for i in range(4)])+1)

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
  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL, related_name="people")
  job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.SET_NULL, related_name="employees")

  name = models.CharField(max_length=60)
  stamina = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9)])
  charisma = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9)])
  musical_talent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9)])
  tech_talent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9)])
  happiness = models.CharField(max_length=1, default="6", choices=HAPPINESS_LEVELS)
  popularity = models.PositiveSmallIntegerField(default=0)

  # Character appearance settings
  hair_color = models.CharField(max_length=7, default=HAIR_COLORS)
  hair_detail = models.CharField(max_length=7, default=HAIR_COLORS)
  hair_style = models.CharField(max_length=1, default=HAIR_STYLES)
  skin_color = models.CharField(max_length=7, default=SKIN_COLORS)
  shirt_color = models.CharField(max_length=7, default=CLOTHING_COLORS)
  shirt_detail = models.CharField(max_length=7, default=CLOTHING_COLORS)
  shirt_style = models.CharField(max_length=1, default=SHIRT_STYLES)
  jacket_color = models.CharField(max_length=7, default=CLOTHING_COLORS)
  
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "person"
    verbose_name_plural = "contacts"

  def __str__(self):
    return self.name

  @property
  def level(self):
    if self.popularity < 3: return 0
    if self.popularity < 5: return 1
    if self.popularity < 8: return 2
    if self.popularity < 13: return 3
    if self.popularity < 21: return 4
    if self.popularity < 34: return 5
    if self.popularity < 55: return 6
    if self.popularity < 89: return 7
    if self.popularity < 144: return 8

  @property
  def display_attrs(self):
    job = {"title": self.job.role, "workplace": self.job.workplace.name if self.job.workplace else "", "brand_id": self.job.brand_id} if self.job else None
    music_career = self.music_career.first()
    if music_career and self.job:
      job.update({"band_id": music_career.band_id, "band_name": music_career.band.name if music_career.band else None})

    return {
            "genre_id": self.genre.id,
            "location": self.location,
            "id": self.id,
            "job": job,
            "name": self.name,
            "stamina": self.stamina,
            "charisma": self.charisma,
            "musical_talent": self.musical_talent,
            "tech_talent": self.tech_talent,
            "happiness": {"text": self.get_happiness_display(), "value": int(self.happiness)},
            "popularity": self.popularity,
            "level": self.level,
            "appearance": {k: self.__dict__[k] for k in ["hair_color","hair_detail","hair_style","jacket_color","shirt_color","skin_color","shirt_detail","shirt_style"]}
            }