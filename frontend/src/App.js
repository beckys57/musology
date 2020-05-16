import React, { useState, useEffect, useContext } from "react";
import ReactMapGL, { Marker, Popup } from "react-map-gl";
import { ApiDataContext, FnContext } from './Contexts';
import axios from "axios"

export function SidebarContent({venue, postData}) {
  const gameFns = useContext(FnContext)

  return (
    <div className="card">
      <img className="card-img-top" src="/pub.svg" />
      <div className="card-body">
        <h5 className="card-title">{venue.name}</h5>
        <p className="card-text"></p>
    <table key={"venue"+venue.id} className="table card-text">
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
   >

   {markers}

     {children}
   </ReactMapGL>
 );
}

export default function App() {
  const gameContext = useContext(ApiDataContext);
  const [selectedVenue, setSelectedVenue] = useState();
  const [apiData, setApiData] = useState({})
  const [loaded, setLoaded] = useState(false)
  const [sidebarContent, setSidebarContent] = useState();
  const [postData, setPostData] = useState()
  const gameFns = {setApiData: setApiData, setSelectedVenue: setSelectedVenue}

  useEffect(() => {
    function  buildLocationEvents(data) {
      let key;
      let events = {"locations": []}

      for (let i=0; i<data.locations.length; i++) {
        let e = {
          "id": data.locations[i].id, 
          "events": data.locations[i].events,
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
      setLoaded(true)
      setPostData(buildLocationEvents(data))
    }
    getData()
  }, []);

  return (
    <ApiDataContext.Provider value={apiData}>
    <FnContext.Provider value={gameFns}>
      <div id="map" className="col-lg-9">{loaded && <Map>
          {selectedVenue ? ( <VenuePopup selectedVenue={selectedVenue} /> ) : null}
        </Map>}</div>
      <div className="col-lg-3">
        {loaded && selectedVenue ? ( <SidebarContent venue={selectedVenue} postData={postData}></SidebarContent> ) : null}
        <a href="s#" className="btn btn-primary" onClick={function() { takeTurn(gameFns.setApiData, postData) } }>Take turn</a>
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
