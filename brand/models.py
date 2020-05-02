from django.db import models

# Create your models here.
class Brand(models.Model):
  name = models.CharField(max_length=128)

class Band(models.Model):
  name = models.CharField(max_length=128)
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)

  def influence(self):
    # influence as sum of band influence (later, could go up with awesome events)
    sum([m.influence for m in self.members.all()])

  def __str__(self):
    return self.name

class RecordLabel(models.Model):
  name = models.CharField(max_length=128)

  def __str__(self):
    return self.name

class Event(models.Model):
  name = models.CharField(max_length=128)
  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL)
  starts_at = models.DateField()
  ends_at = models.DateField()
  acts = models.ManyToManyField(Band)
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)

  def __str__(self):
    return "{} at {} on {}-{}".format(self.name, self.location, self.starts_at, self.ends_at)