from django.db import models
from django.db.models import Sum

# Create your models here.
class Brand(models.Model):
  game = models.ForeignKey(to='game.Game', null=True, blank=True, on_delete=models.SET_NULL, related_name="brands")
  name = models.CharField(max_length=127)
  colour = models.CharField(max_length=15, default='blue')
  popularity = models.PositiveSmallIntegerField(default=0)
  money = models.SmallIntegerField(default=100)
  events_unlocked = models.ManyToManyField('events.EventType')

  def __str__(self):
    return self.name

  @property
  def display_attrs(self):
    return {"name": self.name, "colour": self.colour, "money": self.money, "popularity": self.popularity}

class BrandedModel(models.Model):
  brand = models.ForeignKey(to='Brand', null=True, blank=True, on_delete=models.SET_NULL)
  popularity = models.PositiveSmallIntegerField(default=0)

  class Meta:
    abstract = True

class Band(BrandedModel):
  name = models.CharField(max_length=127)
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)
  location = models.ForeignKey('locations.location', null=True, blank=True, on_delete=models.SET_NULL)
  popularity = models.PositiveSmallIntegerField(default=0)

  @property
  def total_popularity(self):
    # popularity as sum of band popularity (later, could go up with awesome events)
    return sum([m.person.popularity for m in self.musicians.all()]) + self.popularity

  def __str__(self):
    return self.name

  def load_all_with_popularity(filter_params={}):
    return Band.objects.annotate(band_popularity=Sum('musicians__person__popularity')).filter(**filter_params)

  @property
  def display_attrs(self):
    return {"id": self.id, "name": self.name, "genre_id": self.genre_id, "location_id": self.location_id, "popularity": self.total_popularity}
  

class RecordLabel(BrandedModel):
  name = models.CharField(max_length=127)
  popularity = models.PositiveSmallIntegerField(default=0)

  def __str__(self):
    return self.name
