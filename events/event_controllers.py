import math
from django.db.models import Max

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

    playerBrand = Brand.objects.get(id=1)
    playerBrand.money -= 50
    playerBrand.save()

    return {
            "model": "Person", 
            "id": person.id,
            "text": person.name + "'s shredding skillz have increased!",
            "event_type": params.get('kind'),
            "venue": params.get('location').name
            }

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

    return {
            "model": "Person", 
            "id": person.id,
            "text": person.name + "'s intonation has improved",
            "event_type": params.get('kind'),
            "venue": params.get('location').name
            }


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

  def calculate_outcome(params):
    from brand.models import Band
    # {'slot': 3, 'kind': 'gig', 'band_ids': [2], 'promoter_ids': [], 'people_ids': [], 'location': <Location: Bojo's (music bar (building type))>}
    location = params["location"]
    print("Calculating outcome of gig at {}..".format(location), params)

    bands = Band.load_all_with_influence({"id__in": [int(p[0]) for p in params["band_ids"]]})

    updates = {
      location: {"influence": location.influence}
    }
    
    # Inherit influence from bands if any who played have more influence
    highest_influence = bands.aggregate(max_influence=Max("band_influence"))['max_influence'] or 0
    influence_diff = highest_influence - location.influence
    if influence_diff > 0:
      # 25% of the difference, minimum 1
      updates[location]["influence"] = updates[location]["influence"] + math.ceil(influence_diff/4)

    # How many people came? District analysis
    # Currently location's don't belong to a district. Rectify this.
    # turnout =

    # TODO: this is a wip
    # influence
    # brand
    # genre
    # capacity
    # prestige
    # entry_price

    print("Band 1", bands.first().band_influence)
    print("Updates", updates)
    print("Done", location)
    # Reward: influence & money
    # Factors: capacity full, overall capacity
    # Stuff to do with all slots combined should be done at the end, so this should update a growing dict of modifiers
    """
    params eg
    {
      modifiers: {venue_obj: influence: -5, prestige: 1}
    }
    """

