import React, { useState, useEffect, useContext } from "react";
import ReactMapGL, { Source, Layer, Marker, Popup } from "react-map-gl";
import { ApiDataContext, FnContext, StatsContext } from './Contexts';
import axios from "axios"
import geodata from "./bristol.geojson";
import { Pie } from "react-chartjs-2";

const cl = console.log

class TurnData {
  constructor() {
    this.slots = {1: [], 2: [], 3: [], 4: []}
  }

  newEvent() {
    return {"venue_id": null,
      "objects": [
        {
          "model": "",
          "names": [],
        }
      ]
    }
  }

  // isObjAvailable(slotNumber, model, objName) {
  //   let busyObjects = 
  //   this.slots[slotNumber].filter(slot => slot.objects.find(o => o.model === model))
  // }

  availableObjects(slotNumber, model, listToFilter) {
    let busyObjs = this.slots[slotNumber.toString()].map(event => event.objects.filter(o => o.model === model).map(event => event.names)).flat().flat();
    return listToFilter.filter(o => busyObjs.indexOf(o.name) === -1)
  }

  addEvent(id, event) {
    this.slots[id].push(event)
    console.log("Slots updated", this.slots)

  }
}

const turnData = new TurnData();

const GeoJsonLayer = ({data}) => {
  const apiData = useContext(ApiDataContext)
  let districtNames = apiData.city.districts.map(d => d.name);
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
              gameFns.selectSomething({selectFn: gameFns.setSelectedTab, selectVal: tabMap[label]});
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

export function CitySidebarContent() {
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)
  const stats = useContext(StatsContext)
  return (
    <>
    <CardHeader title={apiData.city.name} caption={"Population " + apiData.city.population} img={"/band.svg"} />
    <ListOfNamedObjects title="Districts" namedObjects={apiData.city.districts} selectorFn="setSelectedDistrict" />
    <ListOfNamedObjects title="Brands" namedObjects={Object.values(apiData.brands)} selectorFn={null} />
    </>
  )
}

function getAvailableMusicians({slotNumber}) {
  const apiData = useContext(ApiDataContext);
  const gameFns = useContext(FnContext);
  const musicians = apiData.people.filter(person => person.job && person.job.title === "musician");
  let busyMusicians = [];//gameFns.slotData[slotNumber.toString()].objects.filter(o => o.model === "Musician")
  let busyMusicianNames = [];//busyMusicians.map(m => m.names).flat();
  return musicians.filter(m => busyMusicianNames.indexOf(m.name) === -1)
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
    <ListOfNamedObjects title="Members" namedObjects={band_members} selectorFn="setSelectedPerson" />
    </>
  )
}

export function BandsSidebarContent() {
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)
  return (
    <>
    <CardHeader title="Bands" caption={null} img={"/band.svg"} />
    <ListOfNamedObjects title={null} namedObjects={apiData.bands} selectorFn="setSelectedBand" />
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
                      gameFns.selectSomething({selectFn: gameFns.setSelectedBand, selectVal: band});
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

function ListOfNamedObjects({title, namedObjects, selectorFn}) {
  const gameFns = useContext(FnContext)
  return (
      <div className="row">
        <div className="col col-12">
          <div className="card-text">
            <table className="table">
              <thead>
                {title && <tr><th>{title}</th></tr>}
              </thead>
              <tbody>
              {namedObjects.map(obj => (
                <tr key={"obj"+obj.name}>
                  <td>
                    {selectorFn ?
                      <a onClick={e => {
                        e.preventDefault();
                        gameFns.selectSomething({selectFn: gameFns[selectorFn], selectVal: obj});
                      }}>{obj.name}</a>
                      : obj.name
                    }
                  </td>
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
    <ListOfNamedObjects title="People" namedObjects={apiData.people} selectorFn="setSelectedPerson" />
    </>
  )
}

function PieChart({percentages, colours, labels}) {

  return (
    <Pie data={{
              labels: labels,
              datasets: [{
                data: percentages,
                backgroundColor: colours, //["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
                hoverBackgroundColor: colours, //["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
              }]
        }} />
  )
}

export function DistrictSidebarContent({district}) {
  const apiData = useContext(ApiDataContext)
  const genre_ids = [...Array(Object.keys(apiData.genres).length).keys()]

  let percentages = genre_ids.map(function(i) {
    let crowd = district.crowds.find(c => c.genre_id === i+1)
    return (crowd ? crowd.proportion : 0)
  });

  let colours = genre_ids.map(function(i) {
    let crowd = district.crowds.find(c => c.genre_id === i+1)
    return (crowd ? crowd.colour : "#EEEEEE")
  });

  let labels = Object.values(apiData.genres).map(i => i.name)

  return (
    <>
    <CardHeader title={district.name} caption={null} img="/map.jpg" />
    <PieChart percentages={percentages} colours={colours} labels={labels} />
    </>
  )
}

function SlotBar({venue, numOfSlots}) {
  const gameFns = useContext(FnContext);
  let labels = [...Array(numOfSlots+1).keys()].slice(1).map(function z(label) {
      return (
        <button 
          onClick={e => {
                    e.preventDefault();
                    console.log("Clicked")
                    gameFns.setSelectedEvent(label)
                  }}
          key={"slot"+label} type="button" class="btn btn-secondary">{label}</button>
      )});

  return (
    <div class="btn-group" role="group" aria-label="Basic example" style={{width: "100%"}}>{labels}</div>
  )
}

function DropDown({options}) {
  return (
      <select id={options[0]} class="dropdown">
          {options.map(o => (
            <option key={o} >{o}</option>
          ))}
      </select>
    )
}

function EventPlannerForm({slotNumber, venue, eventTemplate}) {
  const apiData = useContext(ApiDataContext)
  let fields;
  if (eventTemplate === null) {
    fields = <DropDown options={venue.event_options.map(e => e.type)} />
  } else {
    // let availableMusicianNames = getAvailableMusicians({slotNumber: slotNumber}).map(m => m.name);
    let availableMusicians = turnData.availableObjects(slotNumber, "Musician", apiData.people.filter(person => person.job && person.job.title === "musician"));
    let availableMusicianNames = availableMusicians.map(m => m.name);
    console.log('Avail', availableMusicianNames)
    fields = <>
          <div>Book a {eventTemplate.type}</div>
          {eventTemplate.requirements.objects.map(function z(r) {
            if (r.model !== "Location") {
              return (
                <>
                <p>{r.model}</p>
                <DropDown options={availableMusicianNames} />
                <button className="btn btn-primary" onClick={e => {
                    e.preventDefault();
                    let event = turnData.newEvent()
                    event.venue_id = venue.id
                    event.objects.push({
                       "model": "Musician",
                       "names": [document.getElementById(availableMusicianNames[0]).value],
                     })
                    turnData.addEvent(slotNumber, event);
                  }
                }>Book</button>
                </>
                )
            }
            return null
          })}
          </>
  }
  return (
      <form>
        {fields}
      </form>
    )
}

export function VenueSidebarContent({venue, selectedEvent}) {
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
      <h5>Events</h5>

      {selectedEvent
        ?
        <EventPlannerForm slotNumber="1" venue={venue} eventTemplate={venue.event_options.length === 1 ? venue.event_options[0] : null} />
        :
        <SlotBar venue={venue} numOfSlots={venue.slots_available}/>
      }
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
                gameFns.setHoveredVenue(null);
                gameFns.selectSomething({selectFn: setSelectedVenue, selectVal: venue});
              }}
              onMouseEnter={e => {
                e.preventDefault();
                gameFns.setHoveredVenue(venue);
              }}
              onMouseLeave={e => {
                e.preventDefault();
                gameFns.setHoveredVenue(null);
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
        gameFns.selectSomething({selectFn: gameFns.setSelectedCity, selectVal: true});
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
                  gameFns.selectSomething({selectFn: setSelectedDistrict, selectVal: apiData.city.districts.find(d => d.name == e.features[0].properties["cmwd11nm"])});
                  // console.log("lngLat", e.lngLat)
                } else {
                  gameFns.selectSomething({selectFn: gameFns.setSelectedCity, selectVal: true});
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

  const [loaded, setLoaded] = useState(false);
  const [selectedTab, setSelectedTab] = useState();
  const [selectedCity, setSelectedCity] = useState(true);
  const [selectedPerson, setSelectedPerson] = useState();
  const [selectedBand, setSelectedBand] = useState();
  const [selectedEvent, setSelectedEvent] = useState();
  const [selectedVenue, setSelectedVenue] = useState();
  const [hoveredVenue, setHoveredVenue] = useState();
  const [selectedDistrict, setSelectedDistrict] = useState();
  const [apiData, setApiData] = useState({});
  const [postData, setPostData] = useState({});

  function selectSomething({selectFn, selectVal}) {
    setSelectedTab(null);
    setSelectedPerson(null);
    setSelectedBand(null);
    setSelectedEvent(null);
    setSelectedVenue(null);
    setSelectedDistrict(null);
    setSelectedCity(false);
    selectFn(selectVal)
  }

  const gameFns = {
    "setSelectedPerson": setSelectedPerson,
    "setSelectedBand": setSelectedBand,
    "setSelectedEvent": setSelectedEvent,
    "setSelectedTab": setSelectedTab,
    "setSelectedCity": setSelectedCity,
    "setSelectedDistrict": setSelectedDistrict,
    "setSelectedVenue": setSelectedVenue,
    "setHoveredVenue": setHoveredVenue,
    "selectSomething": selectSomething,
  }
  
  useEffect(() => {
    // WIP:
    // function crowdData(apiData) {
    //   apiData.city.districts.map(function z(district) {
    //     const genre_ids = [...Array(Object.keys(apiData.genres).length).keys()] 
   
    //     let percentages = genre_ids.map(function(i) {
    //       let crowd = district.crowds.find(c => c.genre_id == i+1)
    //       return (crowd ? crowd.proportion : 0)
    //     }); 
   
    //     let colours = genre_ids.map(function(i) {
    //       let crowd = district.crowds.find(c => c.genre_id == i+1)
    //       return (crowd ? crowd.colour : "#EEEEEE")
    //     }); 
   
    //     let labels = Object.values(apiData.genres).map(i => i.name) 
   
    //     return {
    //             district_id: district.id,
    //             percentages: percentages,
    //             colours: colours,
    //             labels: labels,
    //           }

    //   });
    // }


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
    <StatsContext.Provider value={null}>
      <div id="map" className="col col-9">
        {loaded && <Map>{hoveredVenue ? ( <VenuePopup selectedVenue={hoveredVenue} /> ) : null} {<GeoJsonLayer data={geodata}/>}</Map>}
      </div>
      <div id="sidebar" className="col col-3">
        <div className="card text-center">
          <div className="card-header">
            <SidebarTabs selectedTab={selectedTab} />
          </div>
          <div className="card-body overflow-auto" style={{height: "80vh"}}>
            {loaded && selectedCity ? <CitySidebarContent /> : null}
            {loaded && selectedVenue ? ( <VenueSidebarContent venue={selectedVenue} selectedEvent={selectedEvent}></VenueSidebarContent> ) : null}
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
    </StatsContext.Provider>
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
