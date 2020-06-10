import math
from django.db.models import Max, Sum, Avg
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
    available_crowds = District.objects.get(id=int(district_id)).crowd_counts
    gig_genres = {}
    for gig in gigs:
      band = Band.objects.get(id=int(gig["objects"]["Band"][0]))
      gigs_in_genre = gig_genres.get(band.genre_id, [])
      gig_genres[band.genre_id] = gigs_in_genre + [gig]

    print("available_crowds", available_crowds)

    gigs_with_more_data = []
    for crowd_genre_id, crowd_count in available_crowds.items():
      overflow = 0
      gig_list = gig_genres.get(crowd_genre_id)
      # There are gigs matching this crowd's genre. Split the entire crowd between count events
      if gig_list:
        total_venue_popularity = sum([gig["venue_popularity"] for gig in gig_list])
        print("total_venue_popularity for ", crowd_genre_id, total_venue_popularity)
        for g in gigs:
          bands = Band.load_all_with_popularity({"id__in": [int(gid) for gid in g["objects"]["Band"]]})
          potential_attendees = math.floor(crowd_count / total_venue_popularity / g["venue_popularity"] if g["venue_popularity"] > 0 else 0)
          print("potential_attendees", potential_attendees)
          overflow += max(potential_attendees - g["venue_capacity"], 0)
          g.update(attendance=potential_attendees-overflow, bands=bands, location=Location.objects.get(id=int(g["venue_id"])))
          gigs_with_more_data.append(g)
      available_crowds[crowd_genre_id] = overflow

    # Divvy up the remaining folk in the district
    remaining_punters = sum(available_crowds.values())



    print("gigs out", gigs_with_more_data)


    return gigs

  def calculate_outcome(params):
    # TODO: Check people happiness and cancel if any = 0 update on the fly
    from brand.models import Band
    location = params["location"]
    updates = {
      location: {"popularity": location.popularity}
    }
    print("\nCalculating outcome of gig at {}..".format(location), params)
    bands = Band.load_all_with_popularity({"id__in": [int(sid) for sid in params.get("objects")["Band"]]}).order_by('-popularity')
    band_stats = bands.aggregate(max_popularity=Max("band_popularity"), total_popularity=Sum("band_popularity"), avg_popularity=Avg("band_popularity"))
    print("Bands", bands)
    
    # Inherit popularity from bands if any who played have more popularity
    highest_popularity = band_stats['max_popularity'] or 0
    popularity_diff = highest_popularity - location.popularity
    text = "Gig at {}: {} people came.\n ".format(location.name, params["attendance"])
    if popularity_diff > 0:
      # 25% of the difference, minimum 1
      updates[location]["popularity"] = updates[location]["popularity"] + math.ceil(popularity_diff/4)
      text += "{}'s popularity rubbed off on the venue.\n".format(bands[0])


    # Popularity
    capacity_fullness = params["attendance"] / location.capacity
    print("capacity_fullness", capacity_fullness, "band popularity", band_stats['total_popularity'], "proportion full", params["attendance"] * capacity_fullness, "prestige", location.prestige)
    enjoyment = band_stats['avg_popularity'] + location.prestige
    # TODO: Make popularity_modifier a percentage increase, between -50% and +50% more popular but likely a lot less
    # TODO: implement something similar for bands
    # TODO: Change all of this. Ignore prestige
    """
    Prestige affects attendance. In calculate_attendance make an equation for entry_price, prestige and band top popularity
    Popularity only from band popularity. Can put on lots of small bands with low entry price you make money
    Pay more money to book more popular bands.
    """
    popularity_modifier = max(min(1 + ((enjoyment * capacity_fullness) / 100), 1.5), 0.5)
    updates[location]["popularity"] = math.ceil(updates[location]["popularity"] * popularity_modifier)
    # Money
    takings = (location.entry_price * params["attendance"])
    text += "{} enjoyment.\n £{} taken.\n Venue popularity changed by {}.\n".format(enjoyment, takings, updates[location]["popularity"])

    # Apply location updates
    Location.objects.filter(id=location.id).update(**updates[location])

    brand = Brand.objects.get(id=location.brand_id)
    brand.money = brand.money + takings
    brand.save()

    # for band in bands:
    #   band.money += 1
    #   band.save()

    # TODO: this is a wip
    # popularity
    # brand
    # genre
    # capacity
    # prestige
    # entry_price

    print("Updates", updates)
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
