from game.models import Game

def setup():
  from genres.models import Genre
  from genres.models import Genre
  from brand.models import Band
  from locations.models import City
  from locations.models import District
  from people.models import Person, Job, Musician
  from brand.models import Brand
  from tech.models import Tech
  from locations.models import Location, BuildingType, VenueAssessment
  from events.models import EventType

  Genre.objects.get_or_create(**{"name": "Blues", "year_invented": 1905})
  Genre.objects.get_or_create(**{"name": "Jazz", "year_invented": 1920})
  Genre.objects.get_or_create(**{"name": "Classical", "year_invented": 1748})
  brand, _ = Brand.objects.get_or_create(name="Badger Stripes")
  brand2, _ = Brand.objects.get_or_create(name="Rival Records")
  band1, _ = Band.objects.get_or_create(**{"brand_id": brand.id, "name": "Handwash Experience", "genre_id": 1})
  Band.objects.get_or_create(**{"name": "'ERB GIRLS", "genre_id": 1})
  Band.objects.get_or_create(**{"brand_id": 2, "name": "HOLY SHIT", "genre_id": 2})
  City.objects.get_or_create(**{"name": "Bristol", "latitude": "51.454514", "longitude": "-2.587910"})
  District.objects.get_or_create(**{"city_id": 1, "name": "Bedminister"})
  District.objects.get_or_create(**{"city_id": 1, "name": "Clifton"})
  District.objects.get_or_create(**{"city_id": 1, "name": "Easton"})
  District.objects.get_or_create(**{"city_id": 1, "name": "Fishponds"})
  Person.objects.get_or_create(**{"name": "Sheik Yerbouti", "genre_id": 2})
  Person.objects.get_or_create(**{"name": "William Vacation", "genre_id": 3})
  Person.objects.get_or_create(**{"name": "Ted Sawing", "genre_id": 3})
  Person.objects.get_or_create(**{"name": "Badger Davis", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Foe Mistletoe", "genre_id": 2})
  Person.objects.get_or_create(**{"name": "Dirty Sludge", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Eric Schweindriver", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Cartwright Van-Swedehoven", "genre_id": 3})
  Person.objects.get_or_create(**{"name": "Melancoly Carton", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Charlène Splitairi", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Gwen Spaghetti", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Owen Linguini", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Ella Fitsgerbil", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Parsley Erb", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Sage Erb", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Rosemary Erb", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Thyme Erb", "genre_id": 1})

  p1, _=Person.objects.get_or_create(**{"name": "James Handwash", "genre_id": 1})
  p2, _=Person.objects.get_or_create(**{"name": "Yule Bluesman", "genre_id": 1})
  p3, _=Person.objects.get_or_create(**{"name": "Hitch Hitcherson", "genre_id": 1})
  p1.job, _ =Job.objects.get_or_create(**{"role": "musician"})
  p1.save()
  m1, _=Musician.objects.get_or_create(**{"person": p1, "band_id": 1})
  p2.job, _ =Job.objects.get_or_create(**{"role": "musician"})
  p2.save()
  m2, _=Musician.objects.get_or_create(**{"person": p2, "band_id": 1})
  p3.job, _ =Job.objects.get_or_create(**{"role": "musician"})
  p3.save()
  m3, _=Musician.objects.get_or_create(**{"person": p3, "band_id": 1})
  band1.musicians.set([m1,m2,m3])
  t1, _ = Tech.objects.get_or_create(name="open mic", affects="[Venue]", effects="{'prestige': 1}")
  t1.brand.set([brand])
  Tech.objects.get_or_create(name="dishwasher", affects="[Venue]", effects="{'prestige': 1, 'running_costs': 5}")
  music_bar, _ = BuildingType.objects.get_or_create(name='music bar', category='venue with stage')
  pub, _ = BuildingType.objects.get_or_create(name='local pub', category='pub or cafe')
  mschool, _ = BuildingType.objects.get_or_create(name='music school', category='pub or cafe')
  venue, _ = Location.objects.get_or_create(building_type=music_bar, name="Bojo's", genre_id=1, brand_id=2, latitude="51.4686715", longitude="-2.6171386")
  pubvenue, _ = Location.objects.get_or_create(building_type=pub, name="Ye Olde 'Ole", genre_id=2, latitude="51.4630824", longitude="-2.6056613")
  school, _ = Location.objects.get_or_create(building_type=mschool, name="Widow Twankey's Honk & Tonk School", genre_id=1, brand_id=2, latitude="51.4568828", longitude="-2.6063455", capacity=1, slots_available=2)
  event_type, _ = EventType.objects.get_or_create(name='gig', controller="Gig") # Gig
  event_type_lesson, _ = EventType.objects.get_or_create(name='music lesson', controller="MusicLesson") # Gig
  VenueAssessment.objects.get_or_create(suitability=9, building_type=music_bar, event_type=event_type)
  VenueAssessment.objects.get_or_create(suitability=6, building_type=pub, event_type=event_type)
  VenueAssessment.objects.get_or_create(suitability=9, building_type=mschool, event_type=event_type_lesson)

def main():
  game, _ = Game.objects.get_or_create(id=1)
  game.initialize()
