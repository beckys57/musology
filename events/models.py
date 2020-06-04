import math

from django.db import models
from django.db.models import Max
from .event_controllers import *

class EventSlot(models.Model):
  # Usually 4 events can be added to a building's slots. These can be added per turn. Some events can be 
  venue = models.ForeignKey(to='locations.Location', null=True, blank=True, on_delete=models.SET_NULL)
  event = models.ForeignKey(to='Event', null=True, blank=True, on_delete=models.SET_NULL)
  parties_involved = models.ManyToManyField(to='people.Person') # Covers all staff, musicians etc
  brands_involved = models.ManyToManyField(to='brand.Brand')
  bands_involved = models.ManyToManyField(to='brand.Band')

  def __str__(self):
    return "{} event slot".format(self.venue)

class EventType(models.Model):
  # TODO: Make it lambda
  EVENT_KINDS = [
      'gig',
      'tour',
      'party',
      'training',
      'recording',
    ]
  EVENT_CHOICES = [(e,e) for e in EVENT_KINDS]

  name = models.CharField(max_length=27, choices=EVENT_CHOICES, default='gig')
  controller = models.CharField(max_length=15, default='Gig')
  slots_required = models.PositiveSmallIntegerField(default=1)

  def __str__(self):
    return "{} (event type)".format(self.name)

  def calculate_outcome(self, event_data):
    eval(self.controller).calculate_outcome(event_data)

  def unlocked_for_brand(brand_id):
    from tech.models import Tech
    EVENT_KINDS + [t.name for t in Tech.objects.filter(brand_id=brand_id, category='event')]

  def filter_for_location(location):
    # Send locations to check for player
    # Can happen in anyone's location? Yes but maybe the slots are sometimes filled, if you know the venue owner they can reserve slot
    # Venue assessment exists (suitability is 5+?)
    # TODO: Add some initialize functions eg add eventtype needs a venueassessment
    event_types = EventType.objects.filter(venueassessment__building_type_id=location.building_type_id, slots_required__lte=location.slots_available)
    return event_types

  def options_for_location(location, brand_id=None):
    # Return the event type name, slots_required and requirements
    event_types = EventType.filter_for_location(location)
    # build a dict with requirements from controller
    options = []
    for et in event_types:
      requirements = eval(et.controller).requirements
      # Does brand meet requirements? Work out client-side
      # {
      # "objects": [
      #   {"model": 'Band', "min": 1, "max": 5},
      #   {"model": 'Location', "min": 1, "max": 1},
      # ],
      # "staff": [
      #    {"role": "promoter", "min": 0, "max": 1},
      #    {"role": "techie", "min": 1, "max": 2},
      #   ]
      # }

      options.append({"type": et.name, "slots_required": et.slots_required, "requirements": requirements})
    return options


# event outcome - modifies influence, update attributes eg increase capacity, new objects, skill up
class Event(models.Model):
  event_type = models.ForeignKey(EventType, null=True, blank=True, on_delete=models.SET_NULL)
  brand = models.ForeignKey('brand.Brand', null=True, blank=True, on_delete=models.SET_NULL)
  location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
  genre = models.ForeignKey('genres.Genre', null=True, blank=True, on_delete=models.PROTECT)
  people = models.ManyToManyField('people.Person')
  acts = models.ManyToManyField('brand.Band')
  name = models.CharField(max_length=127)

  def __str__(self):
    return "{} at {} on {}-{}".format(self.name, self.location, self.starts_at, self.ends_at)

  def validate_location(self, location):
    # Check 
    return (location.brand_id == 1 or location.building == 'park')




