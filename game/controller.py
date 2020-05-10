# Nearby locations /w/api.php?action=query&format=json&prop=coordinates%7Cpageimages%7Ccategories&generator=geosearch&pilicense=free&ggscoord=51.4520822%7C-2.5970355
import mwclient
import random
import requests

config = {
  "genre_count": 3,
  "musicians_per_genre": 1,
}

class Controller(object):
  def glr(lon, lat):
    # Bristol
    # x = "51.4520822"
    # y = "-2.5970355"
    # Dublin
    # (x,y)=("53.350140","-6.266155")
    url="https://en.wikipedia.org/w/api.php?action=query&format=json&prop=coordinates%7Cpageimages%7Ccategories&generator=geosearch&pilicense=free&ggscoord={}%7C{}".format(lon, lat)

    response = requests.get(url)

    return [p["title"] for pid, p in response.json()['query']["pages"].items() if p.get('categories', False) and ["music" in t for t in [c["title"] for c in p['categories']]]]

  def get_locations_with_requests(x, y):
    url="https://en.wikipedia.org/w/api.php?action=query&format=json&prop=coordinates%7Cpageimages%7Ccategories&generator=geosearch&pilicense=free&ggscoord={}%7C{}".format(x, y)

    response = requests.get(url)

    return {p["title"]: [c["title"] for c in p['categories']] for pid, p in response.json()['query']["pages"].items() if p.get('categories', False) and ["music" in t for t in [c["title"] for c in p['categories']]]}
    # return [p["title"] for pid, p in response.json()['query']["pages"].items() if p.get('categories', False) and ["music" in t for t in [c["title"] for c in p['categories']]]]
    # return {p["title"]: p[] for pid, p in response.json()['query']["pages"].items() if p.get('categories', False) and ["music" in t for t in [c["title"] for c in p['categories']]]}


  def delist_category_title(category_title):
    return category_title.replace('List of ', '').replace(' musicians', '')

  def create_musicians(genres):
    for g, ms in genres.items():
      genres[g] = [m for m in Controller.iter_sample_fast(ms, config["musicians_per_genre"])]
    return genres

  def get_random_genres(site):
    return Controller.iter_sample_fast(site.categories[u'Lists_of_musicians_by_genre'].members(), config["genre_count"])

  def create_genres():
    site = mwclient.Site('en.wikipedia.org')
    # A list of links to categories
    genres = {Controller.delist_category_title(g.name): g.links() for g in Controller.get_random_genres(site)}

    return Controller.create_musicians(genres)
    
  def iter_sample_fast(iterable, samplesize):
    results = []
    iterator = iter(iterable)
    # Fill in the first samplesize elements:
    for _ in range(samplesize):
        results.append(iterator.next())
    random.shuffle(results[3:])  # Randomize their positions
    for i, v in enumerate(iterator, samplesize):
        r = random.randint(0, i)
        if r < samplesize:
            results[r] = v  # at a decreasing rate, replace random items

    if len(results) < samplesize:
        raise ValueError("Sample larger than population.")
    return results
