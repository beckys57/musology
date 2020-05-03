from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

class Crowd(models.Model):
  district = models.ForeignKey('locations.District', null=True, on_delete=models.CASCADE, related_name="crowds")
  genre = models.ForeignKey('genres.Genre', on_delete=models.PROTECT)
  proportion = models.PositiveSmallIntegerField(null=True, blank=True)

  def __str__(self):
    return "{}% {}".format(self.proportion, self.genre)

  @property
  def display_attrs(self):
    return {"genre_id": self.genre.id, "proportion": self.proportion}

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
    return "{} ({})".format(self.role, self.person)

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
  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL, related_name="people")
  job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.SET_NULL, related_name="employees")

  name = models.CharField(max_length=60)
  happiness = models.CharField(max_length=1, null=True, blank=True)
  influence = models.PositiveSmallIntegerField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "person"
    verbose_name_plural = "contacts"

  def __str__(self):
    return self.name