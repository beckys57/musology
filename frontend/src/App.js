import React, { useState, useEffect, useContext } from "react";
import ReactMapGL, { Marker, Popup } from "react-map-gl";
import { ApiDataContext, FnContext } from './Contexts';
import axios from "axios"

export function SidebarContent({venue}) {
  return (
    <div className="card">
      <img className="card-img-top" src="..." alt="Card image cap"/>
      <div className="card-body">
        <h5 className="card-title">Venue: {venue.name}</h5>
        <p className="card-text">Prestige: {venue.stats.prestige.value}</p>
        <a href="s#" className="btn btn-primary" onClick={takeTurn}>Go somewhere</a>
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

export function Map({selectedVenue}) {
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
              <img src="/skateboarding.svg" alt="Skate Venue Icon" />
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

  console.log("Rendering map", selectedVenue)

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

     {selectedVenue ? (
       <VenuePopup selectedVenue={selectedVenue} />
     ) : null}
   </ReactMapGL>
 );
}

export default function App() {
  const gameContext = useContext(ApiDataContext);
  const [selectedVenue, setSelectedVenue] = useState();
  const [apiData, setApiData] = useState({})
  const [map, setMap] = useState()
  const [sidebarContent, setSidebarContent] = useState();
  const [postData, setPostData] = useState()

  useEffect(() => {
    async function getData() {
      let res = await axios.get('http://localhost:8000')
      let data = res.data
      setApiData(data)
      setMap(<Map selectedVenue={selectedVenue}></Map>)
    }
    getData()
  }, [selectedVenue]);

  useEffect(() => {
    if (selectedVenue != null) {
      setMap(<Map selectedVenue={selectedVenue}></Map>)
      setSidebarContent(<SidebarContent venue={selectedVenue}></SidebarContent>);
    }
  }, [selectedVenue]);

  const gameFns = {setSelectedVenue: setSelectedVenue}

  return (
    <ApiDataContext.Provider value={apiData}>
    <FnContext.Provider value={gameFns}>
      <div id="map" className="col-lg-9">{apiData && map}</div>
      <div className="col-lg-3">{sidebarContent}</div>
    </FnContext.Provider>
    </ApiDataContext.Provider>
  )
}

async function takeTurn() {
  // console.log('Taking turn...', postData)
  // let resp = await axios.post('http://localhost:8000/take_turn/', postData)
  // console.log('Turn taken', resp)
}
