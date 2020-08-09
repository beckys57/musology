from django.shortcuts import render
from .models import LocationFeature

# Create your views here.
def create_basic_location_features(location):
  # <path id={feature.name} fill={"url(#"+feature.name+"Pattern)"} stroke="#000000" strokeWidth="5" d={feature.path_d}></path>
  for attrs in [
      {"layer": "1", "name": "floor", "path_d": "M0 278.91L1191 278.91L1191 842L0 842L0 278.91Z", "filepath": "Carbon-Fibre.svg", "width": "15", "height": "15"},
      {"layer": "1", "name": "wall", "path_d": "M0 -2.64L1191 -2.64L1191 278.91L0 278.91L0 -2.64Z", "filepath": "Protruding-Squares-Wallpaper.svg", "width": "100", "height": "100"},
      {"layer": "2", "name": "bar", "path_d": "M0 212.67L595.5 212.67L595.5 354.33L0 354.33L0 212.67Z", "filepath": "inside/bar-1.svg", "width": "100", "height": "100"},
      {"layer": "3", "name": "barStool", "path_d": "M64.25 262.41L126.75 262.41L126.75 401.99L64.25 401.99L64.25 262.41Z", "filepath": "", "width": "100", "height": "100"},
      {"layer": "3", "name": "barStool", "path_d": "M270.22 262.41L332.72 262.41L332.72 401.99L270.22 401.99L270.22 262.41Z", "filepath": "", "width": "100", "height": "100"},
      {"layer": "3", "name": "stage", "path_d": "M563.92 554.5L1191 554.5L1191 842L563.92 842L563.92 554.5Z", "filepath": "", "width": "100", "height": "100"},
    ]:
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

# <path id="floor" fill="url(#floorPattern)" stroke="#000000" strokeWidth="5" d="M0 278.91L1191 278.91L1191 842L0 842L0 278.91Z"></path>
# <path id="wall" fill="url(#wallPattern)" stroke="#000000" strokeWidth="5" d="M0 -2.64L1191 -2.64L1191 278.91L0 278.91L0 -2.64Z"></path>
# <path id="bar" fill="url(#barPattern)" stroke="#000000" strokeWidth="5" d="M0 212.67L595.5 212.67L595.5 354.33L0 354.33L0 212.67Z"></path>
# <path id="wallObj" fill="#f3ff03" stroke="#000000" strokeWidth="5" d="M640.92 82.66L751.33 82.66L751.33 222.24L640.92 222.24L640.92 82.66Z"></path>
# <path id="wallObj" fill="url(#wallObject)" stroke="#000000" strokeWidth="5" d="M792.72 33.07L903.14 33.07L903.14 172.66L792.72 172.66L792.72 33.07Z"></path>
# <path id="wallObj" fill="#f3ff03" stroke="#000000" strokeWidth="5" d="M937.17 101.82L1047.58 101.82L1047.58 241.41L937.17 241.41L937.17 101.82Z"></path>
# <path id="barStool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M64.25 262.41L126.75 262.41L126.75 401.99L64.25 401.99L64.25 262.41Z"></path>
# <path id="barStool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M168.14 262.41L230.64 262.41L230.64 401.99L168.14 401.99L168.14 262.41Z"></path>
# <path id="barStool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M270.22 262.41L332.72 262.41L332.72 401.99L270.22 401.99L270.22 262.41Z"></path>
# <path id="barStool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M374.1 262.41L436.6 262.41L436.6 401.99L374.1 401.99L374.1 262.41Z"></path>
# <path id="drinksCabinet" fill="#bc25b3" stroke="#000000" strokeWidth="5" d="M0 30.99L595.5 30.99L595.5 172.66L0 172.66L0 30.99Z"></path>
# <path id="barLighting" fill="#2d3879" stroke="#000000" strokeWidth="5" d="M0 0L595.5 0L595.5 30.99L0 30.99L0 0Z"></path>
# <path id="stage" fill="#662078" stroke="#000000" strokeWidth="5" d="M563.92 554.5L1191 554.5L1191 842L563.92 842L563.92 554.5Z"></path>
# <path id="soundSystem" fill="#c61f1d" stroke="#000000" strokeWidth="5" d="M937.17 362.24L1076.75 362.24L1076.75 554.5L937.17 554.5L937.17 362.24Z"></path>
# <path id="stageTop" fill="#f54207" stroke="#000000" strokeWidth="5" d="M687.88 -1.17L1191 -1.17L1191 101.82L687.88 101.82L687.88 -1.17Z"></path>
# <path id="stageBack" fill="#f54207" stroke="#000000" strokeWidth="5" d="M1088.01 101.82L1191 101.82L1191 842L1088.01 842L1088.01 101.82Z"></path>
# <path id="stageBottom" fill="#f54207" stroke="#000000" strokeWidth="5" d="M563.92 739.01L1191 739.01L1191 842L563.92 842L563.92 739.01Z"></path>
# <path id="danceFloor" fill="#e881ec" stroke="#000000" strokeWidth="5" d="M0 739.01L563.92 739.01L563.92 842L0 842L0 739.01Z"></path>