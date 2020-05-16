import React, { useState, useEffect, useContext } from "react";
import ReactMapGL, { Marker, Popup } from "react-map-gl";
import { GameContext } from './Contexts';
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

export function VenuePopup ({selectedVenue, setSelectedVenue}) {
  console.log("Poppin up!", selectedVenue)
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



export function Map({selectedVenue, setSelectedVenue, clickOnVenue}) {
  const apiData = useContext(GameContext)

  const [viewport, setViewport] = useState({
    latitude: 0,
    longitude: 0,
    width: "74vw",
    height: "100vh",
    zoom: 0,
  });

  const [markers, setMarkers] = useState(null);
  useEffect(() => {
    async function setupMap() {
      console.log(apiData)
      setViewport({
        ...viewport,
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
              <img src="/skateboarding.svg" alt="Skate Venue Icon" />
            </button>
          </Marker>
        )))
      console.log("data set")
    }
    setupMap();
  }, [apiData])

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
   <>
   
   <div>
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
         <VenuePopup selectedVenue={selectedVenue} setSelectedVenue={setSelectedVenue} />
       ) : null}
     </ReactMapGL>
   </div>

   </>
 );
}

export default function App() {
  const gameContext = useContext(GameContext);
  const [selectedVenue, setSelectedVenue] = useState(null);
  const [apiData, setApiData] = useState({})
  const [map, setMap] = useState()


  useEffect(() => {
    async function getData() {
      let res = await axios.get('http://localhost:8000')
      let data = res.data
      setApiData(data)
      setMap(<Map selectedVenue={selectedVenue} setSelectedVenue={setSelectedVenue} clickOnVenue={clickOnVenue}></Map>)
    }
    getData()
  }, [apiData]);


  // NB: This is just some example data in the correct format, please replace :)
  const [postData, setPostData] = useState({"locations": [
    {
    "id": 1,
    "events": [
    {
    "slot": 1,
    "kind": "gig",
    "band_ids": [1],
    "promoter_ids": [],
    "people_ids": [],
    },
    {
    "slot": 2,
    "kind": "",
    "band_ids": [],
    "promoter_ids": [],
    "people_ids": [],
    },
    {
    "slot": 3,
    "kind": "gig",
    "band_ids": [2],
    "promoter_ids": [],
    "people_ids": [],
    },
    {
    "slot": 4,
    "kind": "deep clean upgrade",
    "band_ids": [],
    "promoter_ids": [],
    "people_ids": [5],
    },
    ],
    "updates": {
    "entry_price": 12,
    "name": "Badger"
    }
    },
    {
    "id": 2,
    "events": [
    {
    "slot": 1,
    "kind": "training",
    "band_ids": [1],
    "promoter_ids": [],
    "people_ids": [15, 16, 17, 18],
    },
    {
    "slot": 2,
    "kind": "training",
    "band_ids": [],
    "promoter_ids": [],
    "people_ids": [15, 16, 17, 18],
    },
    {
    "slot": 3,
    "kind": "training",
    "band_ids": [2],
    "promoter_ids": [],
    "people_ids": [15, 16, 17, 18],
    },
    {
    "slot": 4,
    "kind": "deep clean upgrade",
    "band_ids": [],
    "promoter_ids": [],
    "people_ids": [15, 16, 17, 18],
    },
    ],
    }
    ]})

  const [sidebarContent, setSidebarContent] = useState();

  function clickOnVenue(venue) {
    setSelectedVenue(venue)
    setSidebarContent(<SidebarContent venue={venue}></SidebarContent>)
  }
  return (
    <GameContext.Provider value={apiData}>
    <div id="map" className="col-lg-9">
      {apiData && 
	map
      }</div>
    <div className="col-lg-3">


    {sidebarContent}    
  </div>
  </GameContext.Provider>
  )
}





async function takeTurn() {
  // console.log('Taking turn...', postData)
  // let resp = await axios.post('http://localhost:8000/take_turn/', postData)
  // console.log('Turn taken', resp)
}
