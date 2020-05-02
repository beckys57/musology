from django.db import models

# Create your models here.
class Brand(models.Model):
  name = models.CharField(max_length=128)

class Band(models.Model):
  name = models.CharField(max_length=128)
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)
  musicians = models.ForeignKey('people.Job', null=True, blank=True, on_delete=models.SET_NULL)

  def influence(self):
    # influence as sum of band influence (later, could go up with awesome events)
    sum([m.influence for m in self.members.all()])

  def __str__(self):
    return self.name

class RecordLabel(models.Model):
  name = models.CharField(max_length=128)

  def __str__(self):
    return self.name

# class EventType(models.Model):
#   slots_required = models.PositiveSmallIntegerField()
#   starts_at = models.DateField()
#   ends_at = models.DateField()
#   slots = ....

  # event outcome - modifies influence, update attributes eg increase capacity, new objects, skill up
class Event(models.Model):
  EVENT_KINDS = [
    ('gig', 'gig'),
    ('tour', 'tour'),
    ('party', 'party'),
    ('training', 'training'),
    ('recording', 'recording'),
  ]

  name = models.CharField(max_length=128)
  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
  acts = models.ManyToManyField(Band)
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)
  kind = models.CharField(max_length=10, choices=EVENT_KINDS, default='gig')
  people = models.ManyToManyField('people.Person')

  def __str__(self):
    return "{} at {} on {}-{}".format(self.name, self.location, self.starts_at, self.ends_at)