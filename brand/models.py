from django.db import models

# Create your models here.
class Brand(models.Model):
  game = models.ForeignKey(to='game.Game', null=True, blank=True, on_delete=models.SET_NULL, related_name="brands")
  name = models.CharField(max_length=127)

  def __str__(self):
    return self.name

class BrandedModel(models.Model):
  brand = models.ForeignKey(to='Brand', null=True, blank=True, on_delete=models.SET_NULL)

  class Meta:
    abstract = True

class Band(BrandedModel):
  name = models.CharField(max_length=127)
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)

  def influence(self):
    # influence as sum of band influence (later, could go up with awesome events)
    sum([m.influence for m in self.members.all()])

  def __str__(self):
    return self.name

class RecordLabel(BrandedModel):
  name = models.CharField(max_length=127)

  def __str__(self):
    return self.name

# class EventType(BrandedModel):
#   slots_required = models.PositiveSmallIntegerField()
#   starts_at = models.DateField()
#   ends_at = models.DateField()
#   slots = ....

  # event outcome - modifies influence, update attributes eg increase capacity, new objects, skill up
class Event(BrandedModel):
  EVENT_KINDS = [(e,e) for e in [
      'gig',
      'tour',
      'party',
      'training',
      'recording',
    ]
  ]

  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)
  people = models.ManyToManyField('people.Person')
  acts = models.ManyToManyField(Band)
  name = models.CharField(max_length=127)
  kind = models.CharField(max_length=27, choices=EVENT_KINDS, default='gig')

  def __str__(self):
    return "{} at {} on {}-{}".format(self.name, self.location, self.starts_at, self.ends_at)

  def validate_location(self, location):
    # Check 
    return (location.brand_id == 1 or location.building == 'park')

class Gig(object):
  from people.models import Job, Person
  from locations.models import Location

  requirements = {
      "objects": [
        {"model": Band, "min": 1, "max": 5},
        {"model": Location, "min": 1, "max": 1},
      ],
      "staff": [
         {"role": "promoter", "min": 0, "max": 1},
         {"role": "techie", "min": 1, "max": 2},
        ]
      }

  # def relay_outcome(self):





