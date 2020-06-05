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

  Genre.objects.get_or_create(**{"name": "Blues", "year_invented": 1905, "colour": "#46BFBD"})
  Genre.objects.get_or_create(**{"name": "Jazz", "year_invented": 1920, "colour": "#F7464A"})
  Genre.objects.get_or_create(**{"name": "Classical", "year_invented": 1748, "colour": "#FDB45C"})
  brand, _ = Brand.objects.get_or_create(name="Badger Stripes")
  brand2, _ = Brand.objects.get_or_create(name="Rival Records")
  handwash, _ = Band.objects.get_or_create(**{"brand_id": brand.id, "name": "Handwash Experience", "genre_id": 1})
  erbs, _ = Band.objects.get_or_create(**{"name": "'ERB GIRLS", "genre_id": 1, "influence": 20})
  shit, _ = Band.objects.get_or_create(**{"brand_id": 2, "name": "HOLY SHIT", "genre_id": 2})
  City.objects.get_or_create(**{"name": "Bristol", "latitude": "51.454514", "longitude": "-2.587910"})
  bedminster, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Bedminster"})
  clifton, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Clifton"})
  easton, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Easton"})
  eastville, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Eastville"})
  cotham, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Cotham"})
  knowle, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Knowle"})
  lawrence, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Lawrence"})
  redland, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Redland"})
  southville, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Southville"})
  st_george_west, _ = District.objects.get_or_create(**{"city_id": 1, "name": "St George West"})
  windmill, _ = District.objects.get_or_create(**{"city_id": 1, "name": "Windmill"})
  [district.initialize() for district in District.objects.all()]
  Person.objects.get_or_create(**{"name": "Sheik Yerbouti", "genre_id": 2})
  Person.objects.get_or_create(**{"name": "William Vacation", "genre_id": 3})
  Person.objects.get_or_create(**{"name": "Ted Sawing", "genre_id": 3})
  Person.objects.get_or_create(**{"name": "Badger Davis", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Foe Mistletoe", "genre_id": 2})
  Person.objects.get_or_create(**{"name": "Cartwright Van-Swedehoven", "genre_id": 3})
  Person.objects.get_or_create(**{"name": "Melancoly Carton", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Charlène Splitairi", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Gwen Spaghetti", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Owen Linguini", "genre_id": 1})
  Person.objects.get_or_create(**{"name": "Ella Fitsgerbil", "genre_id": 1})
  musician_job, _ = Job.objects.get_or_create(**{"role": "musician"})
  erb1, _ = Person.objects.get_or_create(**{"name": "Parsley Erb", "genre_id": 1,  "job_id": musician_job.id})
  erb2, _ = Person.objects.get_or_create(**{"name": "Sage Erb", "genre_id": 1,  "job_id": musician_job.id})
  erb3, _ = Person.objects.get_or_create(**{"name": "Rosemary Erb", "genre_id": 1,  "job_id": musician_job.id})
  erb4, _ = Person.objects.get_or_create(**{"name": "Thyme Erb", "genre_id": 1,  "job_id": musician_job.id})
  p1, _=Person.objects.get_or_create(**{"name": "James Handwash", "genre_id": 1, "job_id": musician_job.id})
  p2, _=Person.objects.get_or_create(**{"name": "Yule Bluesman", "genre_id": 1, "job_id": musician_job.id})
  p3, _=Person.objects.get_or_create(**{"name": "Hitch Hitcherson", "genre_id": 1, "job_id": musician_job.id})
  m1, _=Musician.objects.get_or_create(**{"person": p1, "band_id": handwash.id})
  m2, _=Musician.objects.get_or_create(**{"person": p2, "band_id": handwash.id})
  m3, _=Musician.objects.get_or_create(**{"person": p3, "band_id": handwash.id})
  e1, _=Musician.objects.get_or_create(**{"person": erb1, "band_id": erbs.id})
  e2, _=Musician.objects.get_or_create(**{"person": erb2, "band_id": erbs.id})
  e3, _=Musician.objects.get_or_create(**{"person": erb3, "band_id": erbs.id})
  e4, _=Musician.objects.get_or_create(**{"person": erb4, "band_id": erbs.id})

  holy1,_=Person.objects.get_or_create(**{"name": "Dirty Sludge", "genre_id": 2, "job_id": musician_job.id})
  shit2,_=Person.objects.get_or_create(**{"name": "Eric Schweindriver", "genre_id": 2, "job_id": musician_job.id})

  holy2, _=Musician.objects.get_or_create(**{"person": holy1, "band_id": shit.id})
  shit1, _=Musician.objects.get_or_create(**{"person": shit2, "band_id": shit.id})

  t1, _ = Tech.objects.get_or_create(name="open mic", affects="[Venue]", effects="{'prestige': 1}")
  t1.brand.set([brand])
  Tech.objects.get_or_create(name="dishwasher", affects="[Venue]", effects="{'prestige': 1, 'running_costs': 5}")
  concert_hall, _ = BuildingType.objects.get_or_create(name='concert hall', category='venue with stage')
  gig_venue, _ = BuildingType.objects.get_or_create(name='gig venue', category='venue with stage')
  music_bar, _ = BuildingType.objects.get_or_create(name='music bar', category='venue with stage')
  dive_bar, _ = BuildingType.objects.get_or_create(name='dive bar', category='venue without stage')
  pub, _ = BuildingType.objects.get_or_create(name='local pub', category='pub or cafe')
  cafe , _ = BuildingType.objects.get_or_create(name='cafe', category='pub or cafe')
  club, _ = BuildingType.objects.get_or_create(name='club', category='venue_with stage')
  mschool, _ = BuildingType.objects.get_or_create(name='music school', category='pub or cafe')
  guitarshop, _ = BuildingType.objects.get_or_create(name='guitar shop', category='shop')
  venue, _ = Location.objects.get_or_create(building_type=music_bar, name="Bojo's", district_id=cotham.id, genre_id=int(cotham.crowds_in_size_order[0]["genre_id"]), brand_id=2, latitude="51.4656069", longitude="-2.6087273", capacity=120)
  venue2, _ = Location.objects.get_or_create(building_type=pub, name="Dancing Pig", district_id=cotham.id, genre_id=int(cotham.crowds_in_size_order[0]["genre_id"]), brand_id=2, latitude="51.4669147", longitude="-2.6008227", capacity=100)
  Location.objects.get_or_create(building_type=dive_bar, name="Rusty Spoon", district_id=cotham.id, genre_id=int(cotham.crowds_in_size_order[0]["genre_id"]), latitude="51.4380286", longitude="-2.5738362", capacity=80, prestige=0)
  Location.objects.get_or_create(building_type=pub, name="The Baker's Giblets", district_id=cotham.id, genre_id=int(cotham.crowds_in_size_order[0]["genre_id"]), latitude="51.4659809", longitude="-2.6105696", capacity=50, prestige=6)
  Location.objects.get_or_create(building_type=pub, name="Ye Olde 'Ole", district_id=knowle.id, genre_id=int(knowle.crowds_in_size_order[0]["genre_id"]), latitude="51.4697231", longitude="-2.6136605", capacity=30)
  Location.objects.get_or_create(building_type=pub, name="The Black Jack-rabbit", district_id=knowle.id, genre_id=int(knowle.crowds_in_size_order[0]["genre_id"]), latitude="51.4350184", longitude="-2.5714117", capacity=25)
  c, _ = Location.objects.get_or_create(building_type=pub, name="Lady Volvas Cafe", district_id=knowle.id, genre_id=int(knowle.crowds_in_size_order[0]["genre_id"]), latitude="51.4310019", longitude="-2.5714624", capacity=15)
  print("cafe is ", c)

  bliss, _ = Location.objects.get_or_create(building_type=guitarshop, name="Total Bliss", latitude="51.4572499", longitude="-2.596153", capacity=30, slots_available=0)
  school, _ = Location.objects.get_or_create(building_type=mschool, name="Widow Twankey's Honk & Tonk School", brand_id=2, latitude="51.4568828", longitude="-2.6063455", capacity=1, slots_available=2)
  gig, _ = EventType.objects.get_or_create(name='gig', controller="Gig") # Gig
  event_type_lesson, _ = EventType.objects.get_or_create(name='music lesson', controller="MusicLesson") # Gig
  event_type_lesson2, _ = EventType.objects.get_or_create(name='scale practice', controller="ScalePractice") # Gig
  VenueAssessment.objects.get_or_create(suitability=9, building_type=concert_hall, event_type=gig)
  VenueAssessment.objects.get_or_create(suitability=9, building_type=gig_venue, event_type=gig)
  VenueAssessment.objects.get_or_create(suitability=9, building_type=club, event_type=gig)
  VenueAssessment.objects.get_or_create(suitability=7, building_type=music_bar, event_type=gig)
  VenueAssessment.objects.get_or_create(suitability=6, building_type=dive_bar, event_type=gig)
  VenueAssessment.objects.get_or_create(suitability=5, building_type=pub, event_type=gig)
  VenueAssessment.objects.get_or_create(suitability=3, building_type=cafe, event_type=gig)
  VenueAssessment.objects.get_or_create(suitability=9, building_type=mschool, event_type=event_type_lesson)
  VenueAssessment.objects.get_or_create(suitability=9, building_type=mschool, event_type=event_type_lesson2)

def main():
  game, _ = Game.objects.get_or_create(id=1)
  game.initialize()
