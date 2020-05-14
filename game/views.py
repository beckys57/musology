import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Game
from brand.models import Band, Brand
from events.models import EventType
from genres.models import Genre
from locations.models import City, Location

@csrf_exempt
def take_turn(request):
  print("Taking turn...")
  if request.method == "POST":
    data = json.loads(request.body.decode())
  
  payload_example = {
    "locations": [
      {
        "id": 1,
        "events": [
          {
            "slot": 1,
            "kind": "gig",  # EVENT_TYPE
            "band_ids": [1],
            "promoter_ids": [],
            "people_ids": [], # Excludes band musicians, but add this in the backend for bonuses or whatever
          },
          {
            "slot": 2,
            "kind": "", # Leave all fields empty for nothing to occur in this slot
            "band_ids": [],
            "promoter_ids": [],
            "people_ids": [],
          },
          {
            "slot": 3,
            "kind": "gig",
            "band_ids": [2],
            "promoter_ids": [],
            "people_ids": [],
          },
          {
            "slot": 4,
            "kind": "deep clean upgrade",
            "band_ids": [],
            "promoter_ids": [],
            "people_ids": [5], # Bar staff can do cleaning and upgrade work
          },
        ],
        "updates": {
          "entry_price": 12, # Set the new value, overriding whatever is in there
          "name": "Swiss Cheese Cafeeeeé"
        }
      },
      {
        "id": 2,
        "events": [
              {
                "slot": 1,
                "kind": "training",  # EVENT_TYPE
                "band_ids": [1],
                "promoter_ids": [],
                "people_ids": [15, 16, 17, 18], # Excludes band musicians, but add this in the backend for bonuses or whatever
              },
              {
                "slot": 2,
                "kind": "training", # Leave all fields empty for nothing to occur in this slot
                "band_ids": [],
                "promoter_ids": [],
                "people_ids": [15, 16, 17, 18],
              },
              {
                "slot": 3,
                "kind": "training",
                "band_ids": [2],
                "promoter_ids": [],
                "people_ids": [15, 16, 17, 18],
              },
              {
                "slot": 4,
                "kind": "deep clean upgrade",
                "band_ids": [],
                "promoter_ids": [],
                "people_ids": [15, 16, 17, 18], # Bar staff can do cleaning and upgrade work
          },
        ],
      }
    ]
  }

  # Venue attributes - name, location, slots
  """
  # location is a dict with id, events, updates
  eg = {
        id: 1,
        events: [{
          "slot": 1,
          "kind": "gig",  # EVENT_TYPE
          "band_ids": [1],
          "promoter_ids": [],
          "people_ids": [], # Excludes band musicians, but add this in the backend for bonuses or whatever
        }]
        updates: {name: "New name"}
      }
  """
  locations = data.get('locations')

  for location in locations:
    # Run all updates
    l = Location.objects.filter(id=location["id"])
    l.update(**location.get("updates", {}))
    # Sort and group events so they can be logically run. Should this be location at a time or all events? Maybe re-structure if find a reason to
    for event in location.get('events', []):
      # Pass off to EventType to get the controller
      print("event", event["kind"])
      if event["kind"]:
        event["location"] = l.first()
        event_controller = EventType.objects.get(name=event["kind"]).calculate_outcome(event)

  return HttpResponseRedirect('/')



  
def index(request):
  game = Game.objects.first()
  if not game:
    game = Game.objects.create()
    game.initialize()

  city_data = City.build_display_attrs()
  genre_data = {g.id: g.display_attrs for g in Genre.objects.all()}
  brand_data = {b.id: b.display_attrs for b in Brand.objects.all()}
  location_data = [l.display_attrs for l in Location.objects.all()]
  band_data = [b.display_attrs for b in Band.load_all_with_influence()]
  response_data = {
                "genres": genre_data,
                "locations": location_data,
                "city": city_data,
                "bands": band_data,
                "brands": brand_data
      }

  return JsonResponse(
                response_data
            )

# Endpoints to add
  #  VENUE
  #  Staff management - hire from available unemployed pool
  #  Pricing screen
  #  Stats/popularity/influence
  #  Slots, with options available to fill them
  #  PEOPLE
  #  Hire? No, do all from elsewhere  so nothing here.
