from django.db import models

class Game(object):
  cities = models.OneToManyField('locations.City')

  def current_tech(self):
    from tech.models import Tech
    return Tech.objects.filter(name__in=self._current_tech)

  def all_venues(self):
    return [[v for v in c.venues.all()] for c in self.cities.all()]

  def initialize(self):
    self._current_tech = ["open mic"]
    [city.initialize() for city in self.cities.all()]

  def send_datat(self):
    data_example = {
      "venues": {},
      "notifications": [
        {
          "title": "You've won worst venue of the year!",
          "body": "Oh dear.",
          "actions": [], # TODO Later....
        }
      ],
    }

  def take_turn(self, payload):
    payload_example = {
      "venues": {
        1: "slots": {
                      1: {
                        "kind": "gig",  # EVENT_TYPE
                        "band_ids": [1],
                        "promoter_ids": [],
                        "people_ids": [], # Excludes band musicians, but add this in the backend for bonuses or whatever
                      },
                      2: {
                        "kind": "", # Leave all fields empty for nothing to occur in this slot
                        "band_ids": [],
                        "promoter_ids": [],
                        "people_ids": [],
                      },
                      3: {
                        "kind": "gig",
                        "band_ids": [2],
                        "promoter_ids": [],
                        "people_ids": [],
                      },
                      4: {
                        "kind": "deep clean upgrade",
                        "band_ids": [],
                        "promoter_ids": [],
                        "people_ids": [5], # Bar staff can do cleaning and upgrade work
                      },
                    },
          "updates": {
            "entry_price": 12, # Set the new value, overriding whatever is in there
            "name": "Swiss Cheese Cafeeeeé"
          }
      },
      2: "slots": {
                    1: {
                      "kind": "training",  # EVENT_TYPE
                      "band_ids": [1],
                      "promoter_ids": [],
                      "people_ids": [15, 16, 17, 18], # Excludes band musicians, but add this in the backend for bonuses or whatever
                    },
                    2: {
                      "kind": "training", # Leave all fields empty for nothing to occur in this slot
                      "band_ids": [],
                      "promoter_ids": [],
                      "people_ids": [15, 16, 17, 18],
                    },
                    3: {
                      "kind": "training",
                      "band_ids": [2],
                      "promoter_ids": [],
                      "people_ids": [15, 16, 17, 18],
                    },
                    4: {
                      "kind": "deep clean upgrade",
                      "band_ids": [],
                      "promoter_ids": [],
                      "people_ids": [15, 16, 17, 18], # Bar staff can do cleaning and upgrade work
                    },
                  },

    },




# Endpoints to add
#  VENUE
#  Staff management - hire from available unemployed pool
#  Pricing screen
#  Stats/popularity/influence
#  Slots, with options available to fill them
#  PEOPLE
#  Hire? No, do all from elsewhere  so nothing here.

