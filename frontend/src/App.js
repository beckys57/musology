import React, { useState, useEffect, useContext } from "react";
import ReactMapGL, { Source, Layer, Marker, Popup } from "react-map-gl";
import { ApiDataContext, FnContext } from './Contexts';
import axios from "axios"
import geodata from "./bristol.geojson";

const GeoJsonLayer = ({data}) => {
  const fillLayer = {
  id: "fill",
    type: "fill",
    "paint": {
      "fill-color": '#007cbf',
      "fill-opacity": 0,
    },
    filter: ['match', ['get', 'cmwd11nm'], ["Ashley", "Clifton", "Southville"], true, false]
  };

  const lineLayer = {
    id: "line",
    type: "line",
    "paint": {
      "line-color": "#007cbf",
      "line-opacity": 1,
      "line-width": 2,
    },
    filter: ['match', ['get', 'cmwd11nm'], ["Ashley", "Clifton", "Southville"], true, false]
  };

  return (
    <Source type="geojson" data={geodata}>
      <Layer {...fillLayer} onClick={function() {alert("123")}} />
      <Layer {...lineLayer} onClick={function() {alert("123")}} />
    </Source>
  );
};

export function SidebarTabs({selectedTab}) {
  const gameFns = useContext(FnContext)
  const setSelectedTab = gameFns.setSelectedTab

  let labels = ["left", "middle", "right"].map(label =>
      <li class="nav-item">
        <a class="nav-link btn btn-secondary" href="#">{label}</a>
      </li>
    )

  return (

    <ul class="nav nav-tabs">
      {labels}
    </ul>
  )
}

export function DistrictSidebarContent({district}) {
  return (
    <div className="card">
      <img className="card-img-top" src="/pub.svg" />
      <div className="card-body">
        <h5 className="card-title">{district.name}</h5>
        <div>{district}</div>
      </div>
    </div>
  )
}

export function VenueSidebarContent({venue}) {
  return (
    <div className="card">
      <img className="card-img-top" src="/pub.svg" />
      <div className="card-body">
        <h5 className="card-title">{venue.name}</h5>
        <table key={"venue"+venue.id} className="table card-text">
          <thead>
            <th>Stats</th>
          </thead>
          <tbody>
            {Object.keys(venue.stats).map((stat, i) =>
              (
          <tr key={"venue"+venue.id+stat}>
            <th>{venue.stats[stat].label}</th>
            <td>{venue.stats[stat].value}</td>
          </tr>
              ))
            }
          </tbody>
        </table>
        <table key={"events"+venue.id} className="table card-text">
          <thead>
            <th>Events</th>
          </thead>
          <tbody>
          {venue.events.map(evt =>
            (
              <tr key={"venue"+venue.id+evt.slot}>
          <th>{evt.slot}</th>
          <td>{evt.kind}</td>
          <td><button type="button" className="btn btn-primary">Edit</button></td>
              </tr>
            ))
          }
          </tbody>
        </table>
      </div>
    </div>
  )
}

export function VenuePopup({selectedVenue}) {
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)

  let lat = parseFloat(selectedVenue.latitude) 
  let long = parseFloat(selectedVenue.longitude) 
  return (
    <Popup
      latitude={lat}
      longitude={long}
      onClose={() => {
        gameFns.setSelectedVenue(null);
      }}
    >
      <div>
        <h2>{selectedVenue.name}</h2>
        <div>{selectedVenue.stats.prestige.value} {selectedVenue.stats.prestige.label}</div>
      </div>
    </Popup>
  )
}

export function Map({children}) {
  console.log("Loading map")
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)
  let setSelectedVenue = gameFns.setSelectedVenue;
  let setSelectedDistrict = gameFns.setSelectedDistrict;
  const [viewport, setViewport] = useState();
  const [markers, setMarkers] = useState(null);

  useEffect(() => {
    async function setupMap() {
      setViewport({
        width: "74vw",
        height: "100vh",
        latitude: parseFloat(apiData.city.latitude),
        longitude: parseFloat(apiData.city.longitude),
        zoom: 13,
      })

    setMarkers(apiData.locations.map(venue => (
          <Marker
            key={venue.id}
            latitude={parseFloat(venue.latitude)}
            longitude={parseFloat(venue.longitude)}
          >
            <button
              className="marker-btn"
              onClick={e => {
                e.preventDefault();
                setSelectedVenue(venue);
                setSelectedDistrict(null);
              }}
            >
              <img src="/pub.svg" alt="Skate Venue Icon" />
            </button>
          </Marker>
        )))
      console.log("data set")
    }
    setupMap();
  }, [])

  useEffect(() => {
    const listener = e => {
      if (e.key === "Escape") {
        setSelectedVenue(null);
      }
    };
    window.addEventListener("keydown", listener);

    return () => {
      window.removeEventListener("keydown", listener);
    };
  }, []);


  // NB: Commented the map out, as it was complaining about me not having API access to your Mapbox account.
  // Can just put this straight back in and remove the Take turn button above
 return (
   <ReactMapGL
     {...viewport}
     mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
     mapStyle="mapbox://styles/martinalcock/cka03ij0a21e31is0xeki0epq"
     onViewportChange={viewportConfig => {
       setViewport(viewportConfig);
     }}
     onClick={function(e) {
                e.preventDefault();
                if (e.features.length > 0) {
                  console.log(e.features[0].properties["cmwd11nm"])
                  setSelectedDistrict(e.features[0].properties["cmwd11nm"])
                  setSelectedVenue(null);

                  // console.log("lngLat", e.lngLat)
                  //  Then use the name to look up from apiData.districts, where the population and crods info will be!
                }
              }}
   >
     {markers}
     {children}
   </ReactMapGL>
 );
}

export default function App() {

  let polygonPaint = ReactMapGL.FillPaint = {
      'fill-color': "#ff0000",
      'fill-opacity': 0.3
  }

  const [loaded, setLoaded] = useState(false)
  const [selectedTab, setSelectedTab] = useState("left")
  const [selectedVenue, setSelectedVenue] = useState();
  const [selectedDistrict, setSelectedDistrict] = useState();
  const [apiData, setApiData] = useState({})
  const [postData, setPostData] = useState()
  const gameFns = {setSelectedTab: setSelectedTab, setApiData: setApiData, setSelectedDistrict: setSelectedDistrict, setSelectedVenue: setSelectedVenue}

  useEffect(() => {
    function  buildLocationEvents(data) {
      let key;
      let events = {"locations": []}

      for (let i=0; i<data.locations.length; i++) {
        let e = {
          "id": data.locations[i].id, 
          "events": data.locations[i].events,
          "updates": {}
        }
        console.log("Adding ", data.locations[i].name, " events")
        events.locations.push(e)
      };
      return events
    }

    async function getData() {
      let res = await axios.get('http://localhost:8000')
      let data = res.data
      setApiData(data)
      console.log("data", data)
      setLoaded(true)
      setPostData(buildLocationEvents(data))
    }
    getData()
  }, []);

  return (
    <ApiDataContext.Provider value={apiData}>
    <FnContext.Provider value={gameFns}>
      <div id="map" className="col-lg-9">
        {loaded && <Map>{selectedVenue ? ( <VenuePopup selectedVenue={selectedVenue} /> ) : null} {<GeoJsonLayer data={geodata}/>}</Map>}
      </div>
      <div id="sidebar" className="col-lg-3" style={{background: "blue", padding: "0"}}>
        <div class="card text-center">
          <div class="card-header">
            <SidebarTabs selectedTab={selectedTab} />
          </div>
          <div class="card-body" style={{height: "80vh"}}>
            {loaded && selectedVenue ? ( <VenueSidebarContent venue={selectedVenue}></VenueSidebarContent> ) : null}
            {loaded && selectedDistrict ? ( <DistrictSidebarContent district={selectedDistrict}></DistrictSidebarContent> ) : null}
          </div>
          <div class="card-footer text-muted">
            <a href="s#" className="btn btn-primary" onClick={function() { takeTurn(setApiData, postData) } }>Take turn</a>
          </div>
        </div>
      </div>
    </FnContext.Provider>
    </ApiDataContext.Provider>
  )
}

async function takeTurn(setApiData, postData) {
  console.log('Taking turn...', postData)
  let resp = await axios.post('http://localhost:8000/take_turn/', postData)
  console.log('Turn taken', resp.data)
  setApiData(resp.data)
}
