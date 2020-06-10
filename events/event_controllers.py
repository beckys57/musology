import math
from django.db.models import Min, Avg
    # gigs = [{'venue_id': 2, 'kind': 'gig', 'objects': {'Band': ['1'], 'Promoter': [], 'Musician': []}}, {'venue_id': 4, 'kind': 'gig', 'objects': {'Band': ['2'], 'Promoter': [], 'Musician': []}}]
from brand.models import Band, Brand
from locations.models import District, Location


class MusicLesson(object):
  requirements = {
      "money": 50,
      "objects": [
        {"model": 'Musician', "min": 2, "max": 1},
      ],
      "staff": []
      }

  def calculate_outcome(params):
    from people.models import Person
    from brand.models import Brand
    print("Taking a music lesson", params)
    people = Person.objects.filter(id__in=[int(sid) for sid in params.get("objects")["Musician"]])
    for person in people:
      person.musical_talent = person.musical_talent + 5
      person.save()
      print("{} had fun in their lesson".format(person))

    print("That cost £", MusicLesson().requirements["money"])
    return [{
                "model": "Person", 
                "id": person.id,
                "text": person.name + "'s shredding skillz have increased!",
                "event_type": params.get('kind'),
                "venue": params.get('location').name
                }]

class ScalePractice(object):
  requirements = {
      "money": 5,
      "objects": [
        {"model": 'Musician', "min": 1, "max": 1},
      ],
      "staff": []
      }

  def calculate_outcome(params):
    from people.models import Person
    print("Practising scales", params)
    people = Person.objects.filter(id__in=[int(sid) for sid in params.get("objects")["Musician"]])
    for person in people:
      person.musical_talent = person.musical_talent + 1
      person.save()

    return [{
                "model": "Person", 
                "id": person.id,
                "text": person.name + "'s intonation has improved",
                "event_type": params.get('kind'),
                "venue": params.get('location').name
                }]


class Gig(object):
  requirements = {
      "money": 10,
      "objects": [
        {"model": 'Band', "min": 1, "max": 5},
      ],
      "staff": [
         {"role": "promoter", "min": 0, "max": 1},
         {"role": "techie", "min": 1, "max": 2},
        ]
      }

  def calculate_attendance(district_id, gigs):
    if not gigs: return gigs
    # Maybe add popularity of bands and venue on data to save lookups
    # gigs = [{'venue_id': 2, 'kind': 'gig', 'objects': {'Band': ['1'], 'Promoter': [], 'Musician': []}}, {'venue_id': 4, 'kind': 'gig', 'objects': {'Band': ['2'], 'Promoter': [], 'Musician': []}}]
    # district_id 5
    # event {'venue_id': 2, 'kind': 'gig', 'objects': {'Band': ['1'], 'Promoter': [], 'Musician': []}}

    # crowds {2: 60, 1: 28}
    print("# Calculating attendance in District {} #".format(district_id))
    available_crowds = District.objects.get(id=int(district_id)).crowd_counts

    # gig_genres = {}
    gigs_wip = []

    for gig in gigs:
      bands = Band.load_all_with_popularity({"id__in": [int(gid) for gid in gig["objects"]["Band"]]})
      # TODO: Not bands.first() for genre, or maybe actually that's ok
      avg_band_popularity = bands.aggregate(avg_band_popularity=Avg("popularity"))["avg_band_popularity"]
      band = bands.first()
      location = Location.objects.get(id=int(gig["venue_id"]))
      gig.update(genre_id=band.genre_id, bands=bands, location=location, avg_band_popularity=avg_band_popularity)
      # Add to gigs by genre map
      # gigs_in_genre = gig_genres.get(band.genre_id, [])
      # gig_genres[band.genre_id] = gigs_in_genre + [gig]
      # Also add gigs to list
      gigs_wip.append(gig)

    def calculate_appeal(gig):
      value = gig["avg_band_popularity"] / ((gig["location"].entry_price or 4) / 4) + (gig["location"].prestige / 4)
      appeal = (gig["venue_popularity"] * 0.25) * (value * 0.75)
      return appeal
    

    gigs_updated = []
    # Calculate event appeal ratings
    for g in gigs_wip:
      value = calculate_appeal(g)
      appeal = (g["venue_popularity"] * 0.25) * (value * 0.75)
      g.update(appeal=appeal)
      gigs_updated.append(g)

    gigs_wip = gigs_updated
    gigs_updated = []
    for crowd_genre_id, crowd_count in available_crowds.items():
      overflow = 0
      # gig_list = gig_genres.get(crowd_genre_id)
      gig_list = [gig for gig in gigs_wip if gig["genre_id"] == crowd_genre_id]
      # There are gigs matching this crowd's genre. Split the entire crowd between count events
      if gig_list:
        total_venue_popularity = sum([gig["venue_popularity"] for gig in gig_list])
        total_appeal = sum([calculate_appeal(gig) for gig in gig_list])
        for g in gig_list:
          potential_attendees = math.floor(crowd_count / (((total_venue_popularity / g["venue_popularity"]) + (total_appeal / g["appeal"])) / 2) )
          turnaway = max(potential_attendees - g["venue_capacity"], 0)
          actual_attendees = potential_attendees - turnaway
          overflow += turnaway
          g.update(attendance=actual_attendees)
          gigs_updated.append(g)
      available_crowds[crowd_genre_id] = overflow

    remaining_punters = sum(available_crowds.values())
    if remaining_punters > 0:
      # Divvy up the remaining folk in the district
      total_appeal_across_gigs = sum([g["appeal"] for g in gigs_updated])
      gigs_wip = gigs_updated
      gigs_updated = []
      for g in gigs_wip:
        g["attendance"] = g.get("attendance", 0) + math.floor(remaining_punters / total_appeal_across_gigs * g["appeal"])
        gigs_updated.append(g)

    print("gigs out", gigs_updated)
    return gigs_updated

  def calculate_outcome(params):
    # TODO: Check people happiness and cancel if any = 0 update on the fly
    from brand.models import Band
    location = params["location"]
    print("BANDS IN", params["bands"])
    initial_popularity = location.popularity
    updates = {
      location: {"popularity": initial_popularity}
    }
    # print("\nCalculating outcome of gig at {}..".format(location), params)
    bands = Band.load_all_with_popularity({"id__in": [int(sid) for sid in params.get("objects")["Band"]]}).order_by('-popularity').annotate(min_happiness=Min("musicians__person__happiness"))
    # Unhappy bands drop out
    capacity_fullness = params["attendance"] / location.capacity
    dropout_ids = [band.id for band in bands if int(band.min_happiness) < 1]
    if len(dropout_ids) == len(bands):
      updates[location]["popularity"] = updates[location]["popularity"] - math.ceil(5*capacity_fullness)
      return [{
                "model": "Location", 
                "id": location.id,
                "text": "The gig was cancelled because all the bands dropped out!",
                "event_type": params.get('kind'),
                "venue": params.get('location').name,
                "updates": updates
                }]

    gigging_bands = bands.exclude(id__in=dropout_ids)
    gigging_band_stats = gigging_bands.aggregate(avg_band_popularity=Avg("band_popularity"))
    text = "Gig at {}: {} people came.\n ".format(location.name, params["attendance"])

    # Popularity
    # Inherit popularity from bands if average who played have more popularity
    avg_band_popularity = gigging_band_stats['avg_band_popularity']
    crowd_enjoyment = gigging_band_stats['avg_band_popularity'] * capacity_fullness
    popularity_diff = crowd_enjoyment - location.popularity
    # if popularity_diff > 0:
    # 25% of the difference, minimum 1
    updates[location]["popularity"] = updates[location]["popularity"] + math.ceil(popularity_diff/4)
    text += "{} popularity rubbed off on the venue by hosting popular bands.\n".format(math.ceil(popularity_diff/4))


    # print("capacity_fullness", capacity_fullness, "band popularity", gigging_bands['total_popularity'], "proportion full", params["attendance"] * capacity_fullness, "prestige", location.prestige)
    # TODO: implement something similar for bands
    """
    Prestige affects attendance. In calculate_attendance make an equation for entry_price, prestige and band top popularity
    Popularity only from band popularity. Can put on lots of small bands with low entry price you make money
    Pay more money to book more popular bands.
    """
    # popularity_modifier = max(min(1 + ((enjoyment * capacity_fullness) / 100), 1.5), 0.5)
    # Money
    takings = (location.entry_price * params["attendance"])
    text += "£{} taken.\n ".format(takings)

    # Apply location updates
    Location.objects.filter(id=location.id).update(**updates[location])

    brand = Brand.objects.get(id=location.brand_id)
    brand.money = brand.money + takings
    brand.save()

    # Pay bands. Money has already been deducted from Brand. No refunds to venues for no shows, but they don't get paid
    for band in gigging_bands:
      brand = band.brand
      if brand:
        text += "£{} paid out for {} (brand {}).\n ".format(10*band.popularity, band.name, band.brand_id)
        brand.money = brand.money + (10*band.popularity)
        brand.save()

    # Then band popularity modifiers

    # TODO: this is a wip
    # popularity
    # brand
    # genre
    # capacity
    # prestige
    # entry_price

    # print("Updates", updates)
    print("Done\n", location)
    return [{
                "model": "Location", 
                "id": location.id,
                "text": text,
                "event_type": params.get('kind'),
                "venue": params.get('location').name,
                "updates": updates
                }]
    # Reward: popularity & money
    # Factors: capacity full, overall capacity
    # Stuff to do with all slots combined should be done at the end, so this should update a growing dict of modifiers
    """
    params eg
    {
      modifiers: {venue_obj: popularity: -5, prestige: 1}
    }
    """
