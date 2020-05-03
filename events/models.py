from django.db import models


class EventSlot(models.Model):
  # Usually 4 events can be added to a building's slots. These can be added per turn. Some events can be 
  venue = models.ForeignKey(to='locations.Location', null=True, blank=True, on_delete=models.SET_NULL)
  event = models.ForeignKey(to='Event', null=True, blank=True, on_delete=models.SET_NULL)
  parties_involved = models.ManyToManyField(to='people.Person') # Covers all staff, musicians etc
  brands_involved = models.ManyToManyField(to='brand.Brand')
  bands_involved = models.ManyToManyField(to='brand.Band')


# event outcome - modifies influence, update attributes eg increase capacity, new objects, skill up
class Event(models.Model):
  EVENT_KINDS = [(e,e) for e in [
      'gig',
      'tour',
      'party',
      'training',
      'recording',
    ]
  ]

  brand = models.ForeignKey(to='brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)
  people = models.ManyToManyField('people.Person')
  acts = models.ManyToManyField('brand.Band')
  name = models.CharField(max_length=127)
  kind = models.CharField(max_length=27, choices=EVENT_KINDS, default='gig')

  def __str__(self):
    return "{} at {} on {}-{}".format(self.name, self.location, self.starts_at, self.ends_at)

  def validate_location(self, location):
    # Check 
    return (location.brand_id == 1 or location.building == 'park')

class Gig(object):
  from brand.models import Band
  from locations.models import Location
  from people.models import Job, Person

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

  def calculate_outcome(self, params):
    venue = params["location"]
    # Reward: influence & money
    # Factors: capacity full, overall capacity
    # Stuff to do with all slots combined should be done at the end, so this should update a growing dict of modifiers
    """
    params eg
    {
      modifiers: {venue_obj: influence: -5, prestige: 1}
    }
    """





