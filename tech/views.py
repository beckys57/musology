from django.shortcuts import render
from django.http import JsonResponse
from tech.models import LocationFeature


def catalogue(request, location_id):
  features = list(LocationFeature.objects.all().prefetch_related("tech").values())
  return JsonResponse(
                features, safe=False
            )

# Initialise with general tech effect ratings but also possible to have specific to each item
FURNI_TECH = {
  "decor": [
      {
        "affects": "Venue",
        "effects": "{'prestige': 1}",
        "category": "location",
      },
      {
        "affects": "Venue",
        "effects": "{'prestige': 2}",
        "category": "location",
      },
  ],
  "stage": [
      {
        "affects": "Venue",
        "effects": "{'prestige': 1}",
        "category": "location",
      },
      {
        "affects": "Venue",
        "effects": "{'prestige': -1, 'popularity': 3}",
        "category": "location",
      },
  ],
  "venue equipment": [
      {
        "affects": "Venue",
        "effects": "{'prestige': 1}",
        "category": "location",
      },
  ],
  "music equipment": [
      {
        "affects": "Venue",
        "effects": "{'prestige': 1}",
        "category": "location",
      },
  ]
}

POSITIONS = {
  "bar_stool_1": (64, 262),
  "bar_stool_2": (270, 262),
  "bar_stool_3": (164, 262),
  "bar_stool_4": (374, 262),
  "drinks_cabinet": (0, 31),
  "wall_art_1": (640, 82),
  "wall_art_2": (792, 33),
  "wall_art_3": (937, 101),
}

FURNI_PACKS = {
  1: [
      {"layer": "1", "name": "carbon fibre floor", "category": "floor", "path_d": "M0 278.91L1191 278.91L1191 842L0 842L0 278.91Z", "filepath": "Carbon-Fibre.svg", "width": "15", "height": "15"},
      {"layer": "1", "name": "honeycomb walls", "category": "wall", "path_d": "M0 -2.64L1191 -2.64L1191 278.91L0 278.91L0 -2.64Z", "filepath": "Protruding-Squares-Wallpaper.svg", "width": "100", "height": "100"},
      {"layer": "2", "name": "bar", "category": "bar", "path_d": "M0 212.24L595 212.24L595 352.24L0 352.24L0 212.24Z", "filepath": "inside/bar-1.svg", "width": "600", "height": "430"},
    {"layer": "3", "name": "basic bar stool","category": "bar_stool", "path_d": "M64.25 262.41L126.75 262.41L126.75 401.99L64.25 401.99L64.25 262.41Z", "filepath": "basic_bar_stool.svg", "width": "62", "height": "140", "x": POSITIONS["bar_stool_1"][0], "y": POSITIONS["bar_stool_1"][1], "has_border": True},
    {"layer": "3", "name": "basic bar stool","category": "bar_stool", "path_d": "M270.22 262.41L332.72 262.41L332.72 401.99L270.22 401.99L270.22 262.41Z", "filepath": "basic_bar_stool.svg", "width": "62", "height": "140", "x": POSITIONS["bar_stool_2"][0], "y": POSITIONS["bar_stool_2"][1], "has_border": True},
      {"layer": "3", "name": "stage", "category": "stage", "path_d": "M563.92 554.5L1191 554.5L1191 842L563.92 842L563.92 554.5Z", "filepath": "", "width": "100", "height": "100"},],
  2: [
      {"layer": "2", "name": "generic wall art", "category": "wall object", "path_d":"M640.92 82.66L751.33 82.66L751.33 222.24L640.92 222.24L640.92 82.66Z", "filepath": "circle_poster.svg", "width": "110", "height": "140", "x": POSITIONS["wall_art_1"][0], "y": POSITIONS["wall_art_1"][0]},
      # {"layer": "2", "name": "generic wall art", "category": "wall object", "path_d":"M937.17 101.82L1047.58 101.82L1047.58 241.41L937.17 241.41L937.17 101.82Z", "filepath": "", "width": "100", "height": "100", "x": POSITIONS["wall_art_3"][0], "y": POSITIONS["wall_art_3"][0]},
      {"layer": "3", "name": "fancy bar stool","category": "bar_stool", "path_d":"M168.14 262.41L230.64 262.41L230.64 401.99L168.14 401.99L168.14 262.41Z", "filepath": "inside/stool-1.svg", "width": "100", "height": "100", "x": POSITIONS["bar_stool_3"][0], "y": POSITIONS["bar_stool_3"][1], "has_border": True},
      {"layer": "3", "name": "fancy bar stool","category": "bar_stool", "path_d":"M374.1 262.41L436.6 262.41L436.6 401.99L374.1 401.99L374.1 262.41Z", "filepath": "inside/stool-1.svg", "width": "100", "height": "100", "x": POSITIONS["bar_stool_4"][0], "y": POSITIONS["bar_stool_4"][1], "has_border": True},
      {"layer": "2", "name": "drinks cabinet", "category": "drinks_cabinet", "path_d":"M0 30.99L595 30.99L595 170.99L0 170.99L0 30.99Z", "filepath": "inside/drinks.svg","width": "26", "height": "140", "x": POSITIONS["drinks_cabinet"][0], "y": POSITIONS["drinks_cabinet"][1]},
      # {"layer": "3", "name": "neon bar lighting", "category": "bar_lighting", "path_d":"M0 0L595 0L595 30.96L0 30.96L0 0Z", "filepath": "", "width": "100", "height": "100"},
      # {"layer": "3", "name": "sound system", "category": "sound_system", "path_d":"M937.17 362.24L1076.75 362.24L1076.75 554.5L937.17 554.5L937.17 362.24Z", "filepath": "", "width": "100", "height": "100"},
      # {"layer": "4", "name": "off-white stage lights (top)", "category": "stage_top", "path_d":"M687.88 -1.17L1191 -1.17L1191 101.82L687.88 101.82L687.88 -1.17Z", "filepath": "", "width": "100", "height": "100"},
      # {"layer": "4", "name": "off-white stage lights (back)", "category": "stage_back", "path_d":"M1088.01 101.82L1191 101.82L1191 842L1088.01 842L1088.01 101.82Z", "filepath": "", "width": "100", "height": "100"},
      # {"layer": "4", "name": "off-white stage lights (bottom)", "category": "stage_bottom", "path_d":"M563.92 739.01L1191 739.01L1191 842L563.92 842L563.92 739.01Z", "filepath": "", "width": "100", "height": "100"},
      # {"layer": "3", "name": "dance floor", "category": "dance_floor", "path_d":"M0 739.01L563.92 739.01L563.92 842L0 842L0 739.01Z", "filepath": "", "width": "100", "height": "100"},
  ],
  "poster pack": [
      {"layer": "2", "name": "generic wall art", "category": "wall object", "path_d":"M792.72 33.07L903.14 33.07L903.14 172.66L792.72 172.66L792.72 33.07Z", "filepath": "", "width": "100", "height": "100", "x": POSITIONS["wall_art_2"][0], "y": POSITIONS["wall_art_2"][0]},
  ]
}

def initialise_tech():
  from tech.models import Tech
  for name, furnis in FURNI_TECH.items():
    for attrs in furnis:
      attrs.update(name=name)
      tech, _ = Tech.objects.get_or_create(**attrs)

def assign_initial_techs():
  from tech.models import Tech
  decor_tech = Tech.objects.filter(name="decor").first()
  stage_tech = Tech.objects.filter(name="stage").first()
  equipment_tech = Tech.objects.filter(name="equipment").first()
  music_tech = Tech.objects.filter(name="music equipment").first()
  # Start with no tech effects on "bar stool", "wallObj", "drinksCabinet", "barLighting"
  LocationFeature.objects.filter(name__in=["floor", "wall", "bar"]).update(tech=decor_tech)
  LocationFeature.objects.filter(name__in=["stage", "danceFloor"]).update(tech=stage_tech)
  LocationFeature.objects.filter(name__in=["stageTop", "stageBack", "stageBottom"]).update(tech=equipment_tech)
  LocationFeature.objects.filter(name__in=["soundSystem"]).update(tech=music_tech)

def load_furni_pack(pack_number, location):
  # <path id={feature.name} fill={"url(#"+feature.name+"Pattern)"} stroke="#000000" strokeWidth="5" d={feature.path_d}></path>
  for attrs in FURNI_PACKS[pack_number]:
      feature, _ = LocationFeature.objects.get_or_create(**attrs) 
      location.features.add(feature)

   # <pattern id="floorPattern" patternUnits="userSpaceOnUse" width="15" height="15">
   #          <image href="/Carbon-Fibre.svg" x="0" y="0" width="15" height="15"/>
   #        </pattern>
   #        <pattern id="wallPattern" patternUnits="userSpaceOnUse" width="100" height="100">
   #          <image href="/Protruding-Squares-Wallpaper.svg" x="0" y="0" width="100" height="100" />
   #        </pattern>
   #        <pattern id="wallObject" patternUnits="userSpaceOnUse" width="56" height="100">
   #          <image href="/Honeycomb-Art.svg" x="0" y="0" width="56" height="100"/>
   #        </pattern>
   #              <pattern id={featurePattern.name +"Pattern"} key={featurePattern.name +"Pattern"} patternUnits="userSpaceOnUse" width={featurePattern.width} height={featurePattern.height}>
   #                <image href={"/"+featurePattern.filepath} x="0" y="0" width={featurePattern.width} height={featurePattern.height}/>
   #              </pattern>

# def load_pack_2(location):
#   for attrs in [
#         {"layer": "1", "name": "wallObj", "path_d":"M640.92 82.66L751.33 82.66L751.33 222.24L640.92 222.24L640.92 82.66Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "wallObj", "path_d":"M792.72 33.07L903.14 33.07L903.14 172.66L792.72 172.66L792.72 33.07Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "wallObj", "path_d":"M937.17 101.82L1047.58 101.82L1047.58 241.41L937.17 241.41L937.17 101.82Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "bar stool", "path_d":"M168.14 262.41L230.64 262.41L230.64 401.99L168.14 401.99L168.14 262.41Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "bar stool", "path_d":"M374.1 262.41L436.6 262.41L436.6 401.99L374.1 401.99L374.1 262.41Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "drinksCabinet", "path_d":"M0 30.99L595.5 30.99L595.5 172.66L0 172.66L0 30.99Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "barLighting", "path_d":"M0 0L595.5 0L595.5 30.99L0 30.99L0 0Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "soundSystem", "path_d":"M937.17 362.24L1076.75 362.24L1076.75 554.5L937.17 554.5L937.17 362.24Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "stageTop", "path_d":"M687.88 -1.17L1191 -1.17L1191 101.82L687.88 101.82L687.88 -1.17Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "stageBack", "path_d":"M1088.01 101.82L1191 101.82L1191 842L1088.01 842L1088.01 101.82Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "stageBottom", "path_d":"M563.92 739.01L1191 739.01L1191 842L563.92 842L563.92 739.01Z", "filepath": "", "width": "100", "height": "100"},
#         {"layer": "1", "name": "danceFloor", "path_d":"M0 739.01L563.92 739.01L563.92 842L0 842L0 739.01Z", "filepath": "", "width": "100", "height": "100"},]:
#       feature, _ = LocationFeature.objects.get_or_create(**attrs) 
#       location.features.add(feature)

# <path id="floor" fill="url(#floorPattern)" stroke="#000000" strokeWidth="5" d="M0 278.91L1191 278.91L1191 842L0 842L0 278.91Z"></path>
# <path id="wall" fill="url(#wallPattern)" stroke="#000000" strokeWidth="5" d="M0 -2.64L1191 -2.64L1191 278.91L0 278.91L0 -2.64Z"></path>
# <path id="bar" fill="url(#barPattern)" stroke="#000000" strokeWidth="5" d="M0 212.67L595.5 212.67L595.5 354.33L0 354.33L0 212.67Z"></path>
# <path id="wallObj" fill="#f3ff03" stroke="#000000" strokeWidth="5" d="M640.92 82.66L751.33 82.66L751.33 222.24L640.92 222.24L640.92 82.66Z"></path>
# <path id="wallObj" fill="url(#wallObject)" stroke="#000000" strokeWidth="5" d="M792.72 33.07L903.14 33.07L903.14 172.66L792.72 172.66L792.72 33.07Z"></path>
# <path id="wallObj" fill="#f3ff03" stroke="#000000" strokeWidth="5" d="M937.17 101.82L1047.58 101.82L1047.58 241.41L937.17 241.41L937.17 101.82Z"></path>
# <path id="bar stool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M64.25 262.41L126.75 262.41L126.75 401.99L64.25 401.99L64.25 262.41Z"></path>
# <path id="bar stool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M168.14 262.41L230.64 262.41L230.64 401.99L168.14 401.99L168.14 262.41Z"></path>
# <path id="bar stool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M270.22 262.41L332.72 262.41L332.72 401.99L270.22 401.99L270.22 262.41Z"></path>
# <path id="bar stool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M374.1 262.41L436.6 262.41L436.6 401.99L374.1 401.99L374.1 262.41Z"></path>
# <path id="drinksCabinet" fill="#bc25b3" stroke="#000000" strokeWidth="5" d="M0 30.99L595.5 30.99L595.5 172.66L0 172.66L0 30.99Z"></path>
# <path id="barLighting" fill="#2d3879" stroke="#000000" strokeWidth="5" d="M0 0L595.5 0L595.5 30.99L0 30.99L0 0Z"></path>
# <path id="stage" fill="#662078" stroke="#000000" strokeWidth="5" d="M563.92 554.5L1191 554.5L1191 842L563.92 842L563.92 554.5Z"></path>
# <path id="soundSystem" fill="#c61f1d" stroke="#000000" strokeWidth="5" d="M937.17 362.24L1076.75 362.24L1076.75 554.5L937.17 554.5L937.17 362.24Z"></path>
# <path id="stageTop" fill="#f54207" stroke="#000000" strokeWidth="5" d="M687.88 -1.17L1191 -1.17L1191 101.82L687.88 101.82L687.88 -1.17Z"></path>
# <path id="stageBack" fill="#f54207" stroke="#000000" strokeWidth="5" d="M1088.01 101.82L1191 101.82L1191 842L1088.01 842L1088.01 101.82Z"></path>
# <path id="stageBottom" fill="#f54207" stroke="#000000" strokeWidth="5" d="M563.92 739.01L1191 739.01L1191 842L563.92 842L563.92 739.01Z"></path>
# <path id="danceFloor" fill="#e881ec" stroke="#000000" strokeWidth="5" d="M0 739.01L563.92 739.01L563.92 842L0 842L0 739.01Z"></path>