# Nearby locations /w/api.php?action=query&format=json&prop=coordinates%7Cpageimages%7Ccategories&generator=geosearch&pilicense=free&ggscoord=51.4520822%7C-2.5970355
import mwclient
import random

config = {
  "genre_count": 3,
  "musicians_per_genre": 1,
}

class Controller(object):
  def delist_category_title(category_title):
    return category_title.replace('List of ', '').replace(' musicians', '')

  def create_musicians(genres):
    for g, ms in genres.items():
      genres[g] = [m.name for m in Controller.iter_sample_fast(ms, config["musicians_per_genre"])]
    return genres

  def create_genres():
    site = mwclient.Site('en.wikipedia.org')
    # A list of links to categories
    genres = site.categories[u'Lists_of_musicians_by_genre']
    # return genres.categories()
    # category_list = [c for c in genres.members()]
    genres = {Controller.delist_category_title(g.name): g.links() for g in Controller.iter_sample_fast(genres.members(), config["genre_count"])}
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
