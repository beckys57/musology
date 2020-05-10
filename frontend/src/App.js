import React, { useState, useEffect } from "react";
import ReactMapGL, { Marker, Popup } from "react-map-gl";
import axios from "axios"

export default function App() {
  const [viewport, setViewport] = useState({
    latitude: 0,
    longitude: 0,
    width: "100vw",
    height: "100vh",
    zoom: 0,
  });
  const [selectedVenue, setSelectedVenue] = useState(null);
  const [apiData, setApiData] = useState({})

  useEffect(() => {
    async function getData() {
      let res = await axios.get('http://localhost:8000')
      let data = res.data
      setApiData(data)
        setViewPort({
          latitude: data.city.latitude,
          longitude: city.longitude,
          width: "100vw",
          height: "100vh",
          zoom: 13,
        })
      console.log("data set")
    }
    getData()
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

  return (
    <div>
      <ReactMapGL
        {...viewport}
        mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        mapStyle="mapbox://styles/martinalcock/cka03ij0a21e31is0xeki0epq"
        onViewportChange={viewport => {
          setViewport(viewport);
        }}
      >
        {apiData.locations.map(venue => (
          <Marker
            key={venue.id}
            latitude={venue.latitude}
            longitude={venue.longitude}
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
        ))}

        {selectedVenue ? (
          <Popup
            latitude={selectedVenue.latitude}
            longitude={selectedVenue.longitude}
            onClose={() => {
              setSelectedVenue(null);
            }}
          >
            <div>
              <h2>{selectedVenue.name}</h2>
            </div>
          </Popup>
        ) : null}
      </ReactMapGL>
    </div>
  );
}
