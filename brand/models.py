from django.db import models

# Create your models here.
class Brand(models.Model):
  game = models.ForeignKey(to='game.Game', null=True, blank=True, on_delete=models.SET_NULL, related_name="brands")
  name = models.CharField(max_length=127)
  colour = models.CharField(max_length=15, default='blue')
  events_unlocked = models.ManyToManyField('events.EventType')
  money = models.SmallIntegerField(default=100)

  def __str__(self):
    return self.name

  @property
  def display_attrs(self):
    return {"name": self.name, "colour": self.colour}

class BrandedModel(models.Model):
  brand = models.ForeignKey(to='Brand', null=True, blank=True, on_delete=models.SET_NULL)

  class Meta:
    abstract = True

class Band(BrandedModel):
  name = models.CharField(max_length=127)
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)
  location = models.ForeignKey('locations.location', null=True, blank=True, on_delete=models.SET_NULL)

  def influence(self):
    # influence as sum of band influence (later, could go up with awesome events)
    sum([m.influence for m in self.members.all()])

  def __str__(self):
    return self.name

  @property
  def display_attrs(self):
    return {"id": self.id, "name": self.name, "genre_id": self.genre_id}

class RecordLabel(BrandedModel):
  name = models.CharField(max_length=127)

  def __str__(self):
    return self.name
