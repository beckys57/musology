import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Game
from brand.models import Band, Brand
from events.models import EventType
from events.event_controllers import Gig
from genres.models import Genre
from locations.models import City, Location
from people.models import Person

def take_turn(request):
  print("Taking turn...")
  data = json.loads(request.body.decode())

  Brand.objects.filter(id=1).update(money=data.get('money'))
  print("Updating bank balance to £", data.get('money'))

  outcomes = []
  for location in data.get('locations'):
    # Run all updates
    l = Location.objects.filter(id=location["id"])
    l.update(**location.get("updates", {}))

  # Events grouped by district then slots
  for district_id, eventData in data.get('events', {}).items():
    for slot, events in eventData.items():

      if district_id != "0":
        gigs = [e for e in events if e.get("kind") == "gig"]
        gigs = Gig.calculate_attendance(district_id, gigs)
        for gig in gigs:
          outcomes.append(Gig.calculate_outcome(gig))
      # Pass off to EventType to get the controller
      for event in events:
        print("event", event)
        if event["kind"] and not event["kind"] == "gig":
          event["location"] = Location.objects.get(id=event["venue_id"])
          outcomes.append(EventType.objects.get(name=event["kind"]).calculate_outcome(event))
  return outcomes

@csrf_exempt
def index(request):
  game = Game.objects.first()
  if not game:
    game = Game.objects.create()
    game.initialize()

  outcomes = []
  if request.method == "POST":
    outcomes = take_turn(request)
    print("Outcomes", outcomes)

  city_data = City.build_display_attrs()
  genre_data = {g.id: g.display_attrs for g in Genre.objects.all()}
  brand_data = {b.id: b.display_attrs for b in Brand.objects.all()}
  location_data = [l.display_attrs for l in Location.objects.all()]
  band_data = [b.display_attrs for b in Band.load_all_with_popularity()]
  people_data = [p.display_attrs for p in Person.objects.all()]
  response_data = {
                "genres": genre_data,
                "locations": location_data,
                "city": city_data,
                "bands": band_data,
                "brands": brand_data,
                "people": people_data,
                "outcomes": outcomes,
                # Key is district ID, next slot number,then list of events (eg AI events/riders)
                "preloaded_events": {"5": {"1": [{'venue_id': 2, 'venue_capacity': 100, 'venue_popularity': 1, 'kind': 'gig', 'objects': {'Band': ['1'], 'Promoter': [], 'Musician': []}}], "2": [], "3": [], "4": []}},
      }

  return JsonResponse(
                response_data
            )

# Endpoints to add
  #  VENUE
  #  Staff management - hire from available unemployed pool
  #  Pricing screen
  #  Stats/popularity/popularity
  #  Slots, with options available to fill them
  #  PEOPLE
  #  Hire? No, do all from elsewhere  so nothing here.

# Notes

    # this.slots = {1: [], 2: [], 3: [], 4: []}
    #       {
    #         "venue_id": 1,
    #         "kind": "music lesson",
    #         "objects": {"Band": []},
    #       }



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
