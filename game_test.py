from game.models import Game

def setup():
  from genres.models import Genre
  from genres.models import Genre
  from brand.models import Band
  from locations.models import City
  from locations.models import District
  from people.models import Person, Job, Musician
  from brand.models import Brand

  Genre.objects.create(**{"name": "Blues", "year_invented": 1905})
  Genre.objects.create(**{"name": "Jazz", "year_invented": 1920})
  Genre.objects.create(**{"name": "Classical", "year_invented": 1748})
  brand = Brand.objects.create(name="Badger Stripes")
  brand2 = Brand.objects.create(name="Rival Records")
  band1 = Band.objects.create(**{"brand_id": brand.id, "name": "Handwash Experience", "genre_id": 1})
  Band.objects.create(**{"name": "'ERB GIRLS", "genre_id": 1})
  Band.objects.create(**{"brand_id": 2, "name": "HOLY SHIT", "genre_id": 2})
  City.objects.create(**{"name": "Bristol"})
  District.objects.create(**{"city_id": 1, "name": "Bedminister"})
  District.objects.create(**{"city_id": 1, "name": "Clifton"})
  District.objects.create(**{"city_id": 1, "name": "Easton"})
  District.objects.create(**{"city_id": 1, "name": "Fishponds"})
  Person.objects.create(**{"name": "Sheik Yerbouti", "genre_id": 2})
  Person.objects.create(**{"name": "William Vacation", "genre_id": 3})
  Person.objects.create(**{"name": "Ted Sawing", "genre_id": 3})
  Person.objects.create(**{"name": "Badger Davis", "genre_id": 1})
  Person.objects.create(**{"name": "Foe Mistletoe", "genre_id": 2})
  Person.objects.create(**{"name": "Dirty Sludge", "genre_id": 1})
  Person.objects.create(**{"name": "Eric Schweindriver", "genre_id": 1})
  Person.objects.create(**{"name": "Cartwright Van-Swedehoven", "genre_id": 3})
  Person.objects.create(**{"name": "Melancoly Carton", "genre_id": 1})
  Person.objects.create(**{"name": "Charlène Splitairi", "genre_id": 1})
  Person.objects.create(**{"name": "Gwen Spaghetti", "genre_id": 1})
  Person.objects.create(**{"name": "Owen Linguini", "genre_id": 1})
  Person.objects.create(**{"name": "Ella Fitsgerbil", "genre_id": 1})
  Person.objects.create(**{"name": "Parsley Erb", "genre_id": 1})
  Person.objects.create(**{"name": "Sage Erb", "genre_id": 1})
  Person.objects.create(**{"name": "Rosemary Erb", "genre_id": 1})
  Person.objects.create(**{"name": "Thyme Erb", "genre_id": 1})

  p1=Person.objects.create(**{"name": "James Handwash", "genre_id": 1})
  p2=Person.objects.create(**{"name": "Yule Bluesman", "genre_id": 1})
  p3=Person.objects.create(**{"name": "Hitch Hitcherson", "genre_id": 1})
  p1.job=Job.objects.create(**{"role": "musician"})
  p1.save()
  m1=Musician.objects.create(**{"person": p1, "band_id": 1})
  p2.job=Job.objects.create(**{"role": "musician"})
  p2.save()
  m2=Musician.objects.create(**{"person": p2, "band_id": 1})
  p3.job=Job.objects.create(**{"role": "musician"})
  p3.save()
  m3=Musician.objects.create(**{"person": p3, "band_id": 1})
  band1.musicians.set([m1,m2,m3])
  from tech.models import Tech
  t1 = Tech.objects.create(name="open mic", affects="[Venue]", effects="{'prestige': 1}")
  t1.brand.set([brand])
  Tech.objects.create(name="dishwasher", affects="[Venue]", effects="{'prestige': 1, 'running_costs': 5}")
  from locations.models import Location, Building
  bar = Building.objects.create(name='music bar', category='venue with stage')
  venue = Location.objects.create(building=bar, name="Bojo's", genre_id=1, brand_id=2)


def main():
  game = Game.objects.create()
  game.initialize()
