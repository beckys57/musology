import React, { useState, useEffect, useContext } from "react";
import ReactMapGL, { Source, Layer, Marker, Popup } from "react-map-gl";
import { ApiDataContext, FnContext } from './Contexts';
import axios from "axios"
import geodata from "./bristol.geojson";
import { Pie } from "react-chartjs-2";

const cl = console.log

const GeoJsonLayer = ({data}) => {
  const apiData = useContext(ApiDataContext)
  let districtNames = apiData.city.districts.map(d => d.name);
  cl("districtNames", districtNames)
  const fillLayer = {
  id: "fill",
    type: "fill",
    "paint": {
      "fill-color": '#007cbf',
      "fill-opacity": 0,
    },
    filter: ['match', ['get', 'cmwd11nm'], districtNames, true, false]
  };

  const lineLayer = {
    id: "line",
    type: "line",
    "paint": {
      "line-color": "#007cbf",
      "line-opacity": 1,
      "line-width": 2,
    },
    filter: ['match', ['get', 'cmwd11nm'], districtNames, true, false]
  };

  return (
    <Source type="geojson" data={geodata}>
      <Layer {...fillLayer} onClick={function() {alert("123")}} />
      <Layer {...lineLayer} onClick={function() {alert("123")}} />
    </Source>
  );
};

const tabMap = {
  "✆": (<PeopleSidebarContent />),
  "♫": (<BandsSidebarContent />),
  "$": null,
  "iCal": null
}

export function SidebarTabs({selectedTab}) {
  const gameFns = useContext(FnContext)

  let labels = ["✆", "♫", "$", "iCal"].map(label => 
      <li className="nav-item">
        <a className="nav-link btn btn-secondary"
            href="#"
            onClick={e => {
              e.preventDefault();
              gameFns.nullSelections();
              gameFns.setSelectedTab(tabMap[label]);
            }}>{label}</a>
      </li>
    )

  return (
    <ul className="nav">
      {labels}
    </ul>
  )
}

function CardHeader({title, caption, img}) {
  return (
      <div className="row">
        <div className="col col-8">
          <h2>{title}</h2>
          {caption && <em>{caption}</em> }
        </div>
        <div className="col col-4">
          <img className="card-img-top" src={img} />
        </div>
      </div> 
    )
}

function getBandMembers({band_id}) {
  const apiData = useContext(ApiDataContext);
  return apiData.people.filter(person => person.job && person.job.title === "musician" && person.band_id === band_id);
}

export function BandSidebarContent({band}) {
  const apiData = useContext(ApiDataContext);
  const gameFns = useContext(FnContext);
  let genre = apiData.genres[band.genre_id.toString()];
  let img = "/" + genre.name.toLowerCase() + ".svg";
  let band_members = getBandMembers(band.id);

  return (
    <>
    <CardHeader title={band.name} caption="" img={img} />
    <div className="row">
      <div className="col col-12">
        <div className="card-text">
          <table key={"stats"+band.id} className="table">
            <thead>
              <th>Rock credentials</th>
            </thead>
            <tbody>
              <tr>
                <td>Influence</td>
                <td>{band.influence}</td>
              </tr>              
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <ListOfNamedObjects named_objects={band_members} selectorFn="setSelectedPerson" />
    </>
  )
}

export function BandsSidebarContent() {
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)
  return (
    <>
    <CardHeader title="Bands" caption={null} img={"/band.svg"} />
    <ListOfNamedObjects named_objects={apiData.bands} selectorFn="setSelectedBand" />
    </>
  )
}

export function PersonSidebarContent({person}) {
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)
  let img = (
      (person.job !== null ) && (["bar staff", "musician", "person", "techie"].indexOf(person.job.title) !== -1) ?
      "/" + person.job.title + ".svg" :
      "/person.svg"
    ) 

  let band = (person.job.title === "musician" && person.job.band_id !== null ? apiData.bands.find(b => b.id == person.job.band_id) : null);
  return (
    <>
    <CardHeader title={person.name} caption={person.happiness.text} img={img} />
    <div className="row">
      <div className="col col-12">
        <div className="card-text">
          <table key={"stats"+person.id} className="table">
            <thead>
              <th>Measures of Rad'ness</th>
            </thead>
            <tbody>
              <tr>
                <td>Stamina</td>
                <td>{person.stamina}</td>
              </tr>              
              <tr>
                <td>Charisma</td>
                <td>{person.charisma}</td>
              </tr>              
              <tr>
                <td>Infuence</td>
                <td>{person.influence}</td>
              </tr>                        
              <tr>
                <td>Musical skillz</td>
                <td>{person.musical_talent}</td>
              </tr>                         
              <tr>
                <td>Tech wizardry</td>
                <td>{person.tech_talent}</td>
              </tr>
            </tbody>
          </table>
          {person.job && 
            <table key={"job"+person.id} className="table">
              <thead>
                <th>Job</th>
              </thead>
              <tbody>
                <tr>
                  <td>Title</td>
                  <td>{person.job.title}</td>
                </tr>
                {person.job.band_id &&
                <tr>
                  <td>Band</td>
                  <td>
                    <a onClick={e => {
                      e.preventDefault();
                      gameFns.nullSelections();
                      gameFns.setSelectedBand(band);
                    }}>{person.job.band_name}</a>
                  </td>
                </tr>              
                }           
              </tbody>
            </table>
          }
        </div>
      </div>
    </div>
    </>
  )
}

function ListOfNamedObjects({named_objects, selectorFn}) {
  const gameFns = useContext(FnContext)
  return (
      <div className="row">
        <div className="col col-12">
          <div className="card-text">
            <table className="table">
              <thead>
                <tr><th>Name</th></tr>
              </thead>
              <tbody>
              {named_objects.map(obj => (
                <tr key={"obj"+obj.name}>
                  <td><a onClick={e => {
                    e.preventDefault();
                    gameFns.nullSelections();
                    gameFns[selectorFn](obj);
                  }}>{obj.name}</a></td>
                </tr>
              ))}
              </tbody>
            </table>
          </div>  
        </div>
      </div>
    )
}

export function PeopleSidebarContent() {
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)
  return (
    <>
    <CardHeader title="People" caption={null} img={"/pub.svg"} />
    <ListOfNamedObjects named_objects={apiData.people} selectorFn="setSelectedPerson" />
    </>
  )
}

function PieChart({percentages}) {
  return (
    <Pie data={{
              labels: ["Blues", "Jazz", "Classical"],
              datasets: [{
                data: percentages,
                backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
                hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
              }]
        }} />
  )
}

export function DistrictSidebarContent({district}) {
  const apiData = useContext(ApiDataContext)
  const genre_ids = [...Array(Object.keys(apiData.genres).length).keys()]

  let percentages = genre_ids.map(function(i) {
    let crowd = district.crowds.find(c => c.genre_id == i+1)
    return (crowd ? crowd.proportion : 0)
  });

  return (
    <>
    <CardHeader title={district.name} caption={null} img="/map.jpg" />
    <PieChart percentages={percentages} />
    </>
  )
}

export function VenueSidebarContent({venue}) {
  return (

    <>
      <CardHeader title={venue.name} caption={null} img={venue.type + ".svg"} />

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
    </>
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
  let setSelectedPerson = gameFns.setSelectedPerson;
  let setSelectedTab = gameFns.setSelectedTab;
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

    setMarkers(apiData.locations.map(function z(venue) {
        let img = (
          ["local pub", "music bar", "music school"].indexOf(venue.type) !== -1 ?
          "/" + venue.type + ".svg" :
          "/pub.svg"
        ) 

        return(
          <Marker
            key={venue.id}
            latitude={parseFloat(venue.latitude)}
            longitude={parseFloat(venue.longitude)}
          >
            <button
              className="marker-btn"
              onClick={e => {
                e.preventDefault();
                gameFns.nullSelections();
                setSelectedVenue(venue);
              }}
            >
              <img src={img} />
            </button>
          </Marker>
        )
      }));
      console.log("data set")
    }
    setupMap();
  }, [])

  useEffect(() => {
    const listener = e => {
      if (e.key === "Escape") {
        gameFns.nullSelections();
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
                  gameFns.nullSelections();
                  setSelectedDistrict(apiData.city.districts.find(d => d.name == e.features[0].properties["cmwd11nm"]))

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
  const [selectedTab, setSelectedTab] = useState()
  const [selectedPerson, setSelectedPerson] = useState()
  const [selectedBand, setSelectedBand] = useState()
  const [selectedVenue, setSelectedVenue] = useState();
  const [selectedDistrict, setSelectedDistrict] = useState();
  const [apiData, setApiData] = useState({})
  const [postData, setPostData] = useState()

  function nullSelections() {
    setSelectedTab(null);
    setSelectedPerson(null);
    setSelectedBand(null);
    setSelectedVenue(null);
    setSelectedDistrict(null);
  }

  const gameFns = {
    "setSelectedPerson": setSelectedPerson,
    "setSelectedBand": setSelectedBand,
    "setSelectedTab": setSelectedTab,
    "setSelectedDistrict": setSelectedDistrict,
    "setSelectedVenue": setSelectedVenue,
    "nullSelections": nullSelections
  }
  
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
      <div id="map" className="col col-9">
        {loaded && <Map>{selectedVenue ? ( <VenuePopup selectedVenue={selectedVenue} /> ) : null} {<GeoJsonLayer data={geodata}/>}</Map>}
      </div>
      <div id="sidebar" className="col col-3">
        <div className="card text-center">
          <div className="card-header">
            <SidebarTabs selectedTab={selectedTab} />
          </div>
          <div className="card-body overflow-auto" style={{height: "80vh"}}>
            {loaded && selectedVenue ? ( <VenueSidebarContent venue={selectedVenue}></VenueSidebarContent> ) : null}
            {loaded && selectedDistrict ? ( <DistrictSidebarContent district={selectedDistrict}></DistrictSidebarContent> ) : null}
            {loaded && selectedTab ? selectedTab : null}
            {loaded && selectedPerson ? (<PersonSidebarContent person={selectedPerson} />): null}
            {loaded && selectedBand ? (<BandSidebarContent band={selectedBand} />): null}
          </div>
          <div className="card-footer text-muted">
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
