from django.db import models
from django.db.models import Sum

# Create your models here.
class Brand(models.Model):
  game = models.ForeignKey(to='game.Game', null=True, blank=True, on_delete=models.SET_NULL, related_name="brands")
  name = models.CharField(max_length=127)
  colour = models.CharField(max_length=15, default='blue')
  influence = models.PositiveSmallIntegerField(default=0)
  money = models.SmallIntegerField(default=100)
  events_unlocked = models.ManyToManyField('events.EventType')

  def __str__(self):
    return self.name

  @property
  def display_attrs(self):
    return {"name": self.name, "colour": self.colour, "money": self.money, "influence": self.influence}

class BrandedModel(models.Model):
  brand = models.ForeignKey(to='Brand', null=True, blank=True, on_delete=models.SET_NULL)
  influence = models.PositiveSmallIntegerField(default=0)

  class Meta:
    abstract = True

class Band(BrandedModel):
  name = models.CharField(max_length=127)
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)
  location = models.ForeignKey('locations.location', null=True, blank=True, on_delete=models.SET_NULL)
  influence = models.PositiveSmallIntegerField(default=0)

  @property
  def total_influence(self):
    # influence as sum of band influence (later, could go up with awesome events)
    return sum([m.person.influence for m in self.musicians.all()]) + self.influence

  def __str__(self):
    return self.name

  def load_all_with_influence(filter_params={}):
    return Band.objects.annotate(band_influence=Sum('musicians__person__influence')).filter(**filter_params)

  @property
  def display_attrs(self):
    return {"id": self.id, "name": self.name, "genre_id": self.genre_id, "location_id": self.location_id, "influence": self.total_influence}
  

class RecordLabel(BrandedModel):
  name = models.CharField(max_length=127)
  influence = models.PositiveSmallIntegerField(default=0)

  def __str__(self):
    return self.name
