import React, { useState, useEffect, useContext } from "react";
import ReactMapGL, { Source, Layer, Marker, Popup } from "react-map-gl";
import { ApiDataContext, FnContext, StatsContext } from './Contexts';
import axios from "axios"
import geodata from "./bristol.geojson";
import { Pie } from "react-chartjs-2";
import { Guitar } from "./components/guitars"

class TurnData {
  constructor() {
    this.slots = {"1": [], "2": [], "3": [], "4": []}
    this.locationPostData = []
  }

  newEvent() {
    return {
          "venue_id": null,
          "kind": "",
          "band_ids": [],
          "promoter_ids": [],
          "people_ids": [],
          "musician_ids": [],
        }
  }

  get slotData() {
    return this.slots
  }

  set resetSlots(s) {
    this.slots = s;
    console.log("Reset", this.slots)
  }

  get locations() {
    return this.locationPostData
  }

  set locations(postData) {
    this.locationPostData = postData;
  }

  // isObjAvailable(slotNumber, model, objName) {
  //   let busyObjectNames = 
  //   this.slots[slotNumber].filter(slot => slot.objects.find(o => o.model === model))
  // }

  busyObjectIds(slotNumber, model) {
    console.log('Busying', this.slots[slotNumber.toString()].map(event => event.objects))
    return this.slots[slotNumber.toString()].map(event => event.objects.filter(o => o.model === model).map(m => m.ids)).flat(2);
  }

  getAvailable(slotNumber, model, listToFilter) {
    let busyObjs = turnData.busyObjectIds(slotNumber, model)
    console.log("busyObjs", busyObjs)
    return listToFilter.filter(o => busyObjs.indexOf(o.id) === -1)
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
      <div className="row sidebar-header">
        <div className="col col-9">
          <h2>{title}</h2>
          {caption && <em>{caption}</em> }
        </div>
        <div className="col col-3">
          <img className="card-img-top" src={img} alt={caption} />
        </div>
      </div> 
    )
}

export function CitySidebarContent() {
  const apiData = useContext(ApiDataContext)
  return (
    <>
    <CardHeader title={apiData.city.name} caption={"Population " + apiData.city.population} img={"/band.svg"} />
    <div className="sidebar-scroll">
      <ListOfNamedObjects title="Districts" namedObjects={apiData.city.districts} selectorFn="setSelectedDistrict" />
      <ListOfNamedObjects title="Brands" namedObjects={Object.values(apiData.brands)} selectorFn={null} />
    </div>
    </>
  )
}

// function getAvailableMusicians({slotNumber}) {
//   const apiData = useContext(ApiDataContext);
//   const gameFns = useContext(FnContext);
//   const musicians = apiData.people.filter(person => person.job && person.job.title === "musician");
//   let busyMusicianIds = [];//gameFns.slotData[slotNumber.toString()].objects.filter(o => o.model === "Musician")
//   let busyMusicianNames = [];//busyMusicianIds.map(m => m.ids).flat();
//   return musicians.filter(m => busyMusicianNames.indexOf(m.name) === -1)
// }

function getBandMembers({band_id}) {
  const apiData = useContext(ApiDataContext);
  return apiData.people.filter(person => person.job && person.job.title === "musician" && person.band_id === band_id);
}

export function BandSidebarContent({band}) {
  const apiData = useContext(ApiDataContext);
  let genre = apiData.genres[band.genre_id.toString()];
  let img = "/" + genre.name.toLowerCase() + ".svg";
  let band_members = getBandMembers(band.id);

  return (
    <>
    <CardHeader title={band.name} caption="" img={img} />
    <div className="row sidebar-scroll">
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
  return (
    <>
    <CardHeader title="Bands" caption={null} img={"/band.svg"} />
    <div className="sidebar-scroll">
    <ListOfNamedObjects title={null} namedObjects={apiData.bands} selectorFn="setSelectedBand" />
    </div>
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

  let band = (person.job && person.job.title === "musician" && person.job.band_id !== null ? apiData.bands.find(b => b.id === person.job.band_id) : null);
  return (
    <>
    <CardHeader title={person.name} caption={person.happiness.text} img={img} />
    <div className="row sidebar-scroll">
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
    <div className="sidebar-scroll">
	<ListOfNamedObjects title="People" namedObjects={apiData.people} selectorFn="setSelectedPerson" />
    </div>
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
    <div className="sidebar-scroll">
      <PieChart percentages={percentages} colours={colours} labels={labels} />
    </div>
    </>
  )
}

function SlotBar({venue, numOfSlots}) {
  const gameFns = useContext(FnContext);
  let labels = [...Array(numOfSlots+1).keys()].slice(1).map(function z(label) {
      // console.log('turndata', turnData)
      // console.log('things in slot', label, turnData.slots[label])
      let thingsInSlot = turnData.slots[label].filter(event => event.venue_id === venue.id);
      // console.log('thinginslot?', thingsInSlot.length)
      return (
        <button 
          onClick={e => {
                    e.preventDefault();
                    gameFns.setSelectedEvent(label)
                  }}
          key={"slot"+label} type="button" class="btn btn-secondary">{thingsInSlot.length ? thingsInSlot[0].kind : label}</button>
      )});

  return (
    <div class="btn-group" role="group" aria-label="Basic example" style={{width: "100%"}}>{labels}</div>
  )
}

function DropDown({modelName, options}) {
  let fieldOptions = options.all.map(function z(o) { 
      let option;
      console.log("O",o)
      if (options.disabledIds.indexOf(o.id.toString()) !== -1) {
        option = <option key={o.id} value={o.id} disabled>{o.name}</option>
      } else {
        option = <option key={o.id} value={o.id}>{o.name}</option>
      }
      return (
        <>
        {option}
        </>
      )
  })

  return (
      <select className={"dropdown "+modelName.toLowerCase()+"Field"}>
        <option key="placeholder">Select a {modelName}</option>
        {fieldOptions}
      </select>
    )
}

function EventPlannerForm({slotNumber, venue, eventTemplate}) {
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)
  let fields;
  if (eventTemplate === null) {
    fields = <DropDown modelName="generic" options={{all: venue.event_options.map(e => e.type), disabledIds: [] }} />
  } else {
    // let musicians = apiData.people.filter(person => person.job && person.job.title === "musician");
    // let busyMusicianIds = turnData.busyObjectIds(slotNumber, "Musician");
    // console.log("busyMusicianIds",busyMusicianIds)
    // console.log("model",r.model)
    let options = {
      "musician": {all: apiData.people.filter(person => person.job && person.job.title === "musician"), disabledIds: turnData.busyObjectIds(slotNumber, "Musician")},
      "band": {all: apiData.bands, disabledIds: turnData.busyObjectIds(slotNumber, "Band")},
    }
    console.log("Options",options)
    fields = <>
          <div>Book a {eventTemplate.type}</div>
          {eventTemplate.requirements.objects.map(r => (
              <>
              <p>{r.model}</p>
              <DropDown modelName={r.model} options={options[r.model.toLowerCase()]} />
              </>
          ))}
          <button className="btn btn-primary" onClick={e => {
              e.preventDefault();
              gameFns.selectSomething({selectFn: gameFns.setSelectedVenue, selectVal: venue})
               
              let event = {
                venue_id: venue.id,
                kind: eventTemplate.type,
                objects: [],
                "band_ids": [],
                "promoter_ids": [],
                "people_ids": [],
                "musician_ids": [],
              }

              eventTemplate.requirements.objects.forEach(function x(r) {
                let eventKey = r.model.toLowerCase() + "_ids";
                let ids = Array.from(document.getElementsByClassName(r.model.toLowerCase()+"Field")).map(m => m.value);
                console.log("Saving", eventKey, ids, r.model.toLowerCase()+"Field")
                event[eventKey].push(ids)
                event.objects.push(
                    { 
                         "model": r.model,
                         "ids": ids,
                      }
                  )
                return
              })
              console.log("Eevent",event)

              turnData.addEvent(slotNumber, event);
            }
          }>Book</button>
          </>
  }
  return (
      <form>
        {fields}
      </form>
    )
}

export function ShopSidebarContent({venue}) {
  let shop = venue;
  console.log('Gui', Guitar)
  return (
    <>
      <CardHeader title={shop.name} caption={null} img={shop.type + ".svg"} />
      <div className="sidebar-scroll">
       <Guitar />
      </div>
    </>
  )
}

export function VenueSidebarContent({venue, selectedEvent}) {
  return (
    <>
      <CardHeader title={venue.name} caption={null} img={venue.type + ".svg"} />
      <div className="sidebar-scroll">
      {selectedEvent
        ?
        <EventPlannerForm slotNumber="1" venue={venue} eventTemplate={venue.event_options.length === 1 ? venue.event_options[0] : null} />
        :
        <>
        <table key={"venue"+venue.id} className="table">
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
        <SlotBar venue={venue} numOfSlots={venue.slots_available}/>
        </>
      }
      </div>
    </>
  )
}

export function VenuePopup({selectedVenue}) {
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
          ["guitar shop", "local pub", "music bar", "music school"].indexOf(venue.type) !== -1 ?
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
                gameFns.selectSomething({selectFn: gameFns.setSelectedVenue, selectVal: venue});
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
              <img src={img} alt={venue.name}/>
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
                  gameFns.selectSomething({selectFn: gameFns.setSelectedDistrict, selectVal: apiData.city.districts.find(d => d.name === e.features[0].properties["cmwd11nm"])});
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

  function buildLocationEvents(data) {
    let events = {"locations": []};

    for (let i=0; i<data.locations.length; i++) {
      let e = {
        "id": data.locations[i].id, 
        "updates": {}
      }
      console.log("Adding ", data.locations[i].name, " events")
      events.locations.push(e)
    };
    return events
  }
  
  useEffect(() => {
    // WIP:
    // function crowdData(apiData) {
    //   apiData.city.districts.map(function z(district) {
    //     const genre_ids = [...Array(Object.keys(apiData.genres).length).keys()] 
   
    //     let percentages = genre_ids.map(function(i) {
    //       let crowd = district.crowds.find(c => c.genre_id === i+1)
    //       return (crowd ? crowd.proportion : 0)
    //     }); 
   
    //     let colours = genre_ids.map(function(i) {
    //       let crowd = district.crowds.find(c => c.genre_id === i+1)
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


  

    async function getData() {
      let res = await axios.get('http://localhost:8000');
      let data = res.data;
      setApiData(data);
      console.log("data", data);
      setLoaded(true);
      turnData.locations = buildLocationEvents(data);
    }
    getData();
  }, []);

  return (
    <ApiDataContext.Provider value={apiData}>
    <FnContext.Provider value={gameFns}>
    <StatsContext.Provider value={null}>
      <div id="map" className="col col-9">
        {loaded && <Map>
        {loaded && hoveredVenue ? ( <VenuePopup selectedVenue={hoveredVenue} /> ) : null} {<GeoJsonLayer data={geodata}/>}
        </Map>}
      </div>
      <div id="sidebar" className="col col-3">
        <div className="card text-center">
          <div className="card-header">
            <SidebarTabs selectedTab={selectedTab} />
          </div>
          <div className="card-body">
            {loaded && selectedCity ? <CitySidebarContent /> : null}
            {loaded && selectedVenue ? (selectedVenue.category === "shop" ?
                                         <ShopSidebarContent venue={selectedVenue}></ShopSidebarContent> :
                                         <VenueSidebarContent venue={selectedVenue} selectedEvent={selectedEvent}></VenueSidebarContent>) : null}
            {loaded && selectedDistrict ? ( <DistrictSidebarContent district={selectedDistrict}></DistrictSidebarContent> ) : null}
            {loaded && selectedTab ? selectedTab : null}
            {loaded && selectedPerson ? (<PersonSidebarContent person={selectedPerson} />): null}
            {loaded && selectedBand ? (<BandSidebarContent band={selectedBand} />): null}
          </div>
          <div className="card-footer sidebar-footer text-muted">
            <a href="s#" className="btn btn-primary" onClick={function() { takeTurn(setApiData, buildLocationEvents) } }>Take turn</a>
          </div>
        </div>
      </div>
    </StatsContext.Provider>
    </FnContext.Provider>
    </ApiDataContext.Provider>
  )
}

async function takeTurn(setApiData, buildLocationEvents) {
  let postData = {...turnData.locationPostData, ...{events: turnData.slots}};
  console.log('Taking turn...', postData)
  let resp = await axios.post('http://localhost:8000/take_turn/', postData)
  console.log('Turn taken', resp.data)
  setApiData(resp.data)
  turnData.resetSlots = {"1": [], "2": [], "3": [], "4": []};
  buildLocationEvents(resp.data)
}
