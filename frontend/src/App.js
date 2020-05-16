import React, { useState, useEffect, useContext } from "react";
import ReactMapGL, { Marker, Popup } from "react-map-gl";
import { GameContext } from './Contexts';
import axios from "axios"

export function SidebarContent({venue}) {
  return (
    <div className="card">
      <img className="card-img-top" src="/pub.svg" />
      <div className="card-body">
        <h5 className="card-title">{venue.name}</h5>
        <p className="card-text"></p>
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
        <a href="s#" className="btn btn-primary" onClick={takeTurn}>Do something</a>
      </div>
    </div>
  )
}

export function VenuePopup() {
  console.log('VenuePopup')
  const contextData = useContext(GameContext)
  console.log('contextData', contextData)
  let selectedVenue = contextData.gameState.selectedVenue;
  let setSelectedVenue = contextData.gameState.setSelectedVenue;

  let lat = parseFloat(selectedVenue.latitude) 
  let long = parseFloat(selectedVenue.longitude) 
  return (
    <Popup
      latitude={lat}
      longitude={long}
      onClose={() => {
        setSelectedVenue(null);
      }}
    >
      <div>
        <h2>{selectedVenue.name}</h2>
        <div>{selectedVenue.stats.prestige.value} {selectedVenue.stats.prestige.label}</div>
      </div>
    </Popup>
  )
}

export function Map() {
  const contextData = useContext(GameContext)
  let apiData = contextData.apiData;
  let gameState = contextData.gameState;
  let selectedVenue = gameState.selectedVenue;
  let setSelectedVenue = gameState.setSelectedVenue;
  let clickOnVenue = gameState.clickOnVenue;
  const [viewport, setViewport] = useState();
  const [markers, setMarkers] = useState(null);

  useEffect(() => {
    async function setupMap() {
      console.log(apiData)
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
                clickOnVenue(venue);

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

     {selectedVenue ? (
       <VenuePopup />
     ) : null}
   </ReactMapGL>
 );
}

export default function App() {
  const gameContext = useContext(GameContext);
  const [selectedVenue, setSelectedVenue] = useState(null);
  const [apiData, setApiData] = useState({})
  const [map, setMap] = useState()
  const [sidebarContent, setSidebarContent] = useState();
  const [postData, setPostData] = useState()

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
      setMap(<Map></Map>)
      setPostData(buildLocationEvents(data))
      console.log(postData)
    }

    getData();

  }, []);


  function clickOnVenue(venue) {
    setSelectedVenue(venue)
    setSidebarContent(<SidebarContent venue={venue}></SidebarContent>)
  }

  const [gameState, setGameState] = useState({selectedVenue: selectedVenue, setSelectedVenue: setSelectedVenue, clickOnVenue: clickOnVenue})

  return (
    <GameContext.Provider value={{apiData: apiData, gameState: gameState}}>
      <div id="map" className="col-lg-9">{apiData && map}</div>
      <div className="col-lg-3">{sidebarContent}</div>
    </GameContext.Provider>
  )
}

async function takeTurn() {
  // console.log('Taking turn...', postData)
  // let resp = await axios.post('http://localhost:8000/take_turn/', postData)
  // console.log('Turn taken', resp)
}
