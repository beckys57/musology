import React, { useState, useEffect, useContext } from "react";
import ReactMapGL, { Source, Layer, Marker, Popup } from "react-map-gl";
import { ApiDataContext, FnContext, StatsContext } from './Contexts';
import Select from 'react-select'
import axios from "axios"
import geodata from "./bristol.geojson";
import { Pie } from "react-chartjs-2";
import { Guitar } from "./components/guitars"
import { Character } from "./components/characters"
import styled from "styled-components";

class TurnData {
  constructor() {
    // Example slots without a district
    this.slotData = {"0": {"1": [], "2": [], "3": [], "4": []}}
    this.busyPeopleMap = {"1": [], "2": [], "3": [], "4": []}
    this.busyBandsMap = {"1": [], "2": [], "3": [], "4": []}
    this.locationPostData = []
  }

  get slots() {
    return this.slotData
  }

  set slots(s) {
    this.slotData = s;
  }

  get locations() {
    return this.locationPostData
  }

  set locations(postData) {
    this.locationPostData = postData;
  }

  busyPeopleIds(slotNumber) {
    return this.busyPeopleMap[slotNumber.toString()].flat();
  }

  busyBandIds(slotNumber) {
    return this.busyBandsMap[slotNumber.toString()].flat();
  }

  addEvent(districtId, slotNumber, event) {
    this.slotData[districtId][slotNumber].push(event)
  }

  addBusyPeopleIds(slotNumber, ids) {
    this.busyPeopleMap[slotNumber].push(ids)
  }

  addBusyBandsIds(slotNumber, ids) {
    this.busyBandsMap[slotNumber].push(ids)
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
  "©": (<BrandsSidebarContent />),
  "iCal": null
}

export function SidebarTabs({selectedTab}) {
  const gameFns = useContext(FnContext)

  let labels = ["✆", "♫", "©", "iCal"].map(label => 
      <li key={label} className="nav-item">
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

function CardHeader({title, caption, imgSrc, img}) {
  return (
      <div className="row sidebar-header">
        <div className="col col-9">
          <h5>{title}</h5>
          {caption && <em>{caption}</em> }
        </div>
        <div className="col col-3">
          {img ? img : <img className="card-img-top" src={imgSrc} alt={caption} />}
        </div>
      </div> 
    )
}

export function CitySidebarContent() {
  const apiData = useContext(ApiDataContext)
  return (
    <>
    <CardHeader title={apiData.city.name} caption={"Population " + apiData.city.population} imgSrc={"/band.svg"} />
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

function getBandMembers(band_id) {
  const apiData = useContext(ApiDataContext);
  return apiData.people.filter(person => person.job && person.job.title === "musician" && person.job.band_id === band_id);
}

function getBrandVenues(brand_id) {
  const apiData = useContext(ApiDataContext);
  return apiData.locations.filter(loc => loc.brand_id === brand_id);
}

export function BrandSidebarContent({brand}) {
  let venues = getBrandVenues(brand.id);
  let img = "/brand.svg";

  return (
    <>
    <CardHeader title={brand.name} caption={"Level "+brand.level} imgSrc={img} />
    <div className="sidebar-scroll">
      <div className="row">
        <div className="col col-12">
          <div className="card-text">
            <table key={"stats"+brand.id} className="table">
              <thead>
                <tr><th>Rock credentials</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td>Popularity</td>
                  <td>{brand.popularity}</td>
                </tr>              
              </tbody>
            </table>
	    <ListOfNamedObjects title="Venues" namedObjects={venues} selectorFn="setSelectedVenue" />
	  </div>
        </div>
      </div>
    </div>
    </>
  )
}

export function BandSidebarContent({band}) {
  const apiData = useContext(ApiDataContext);
  let genre = apiData.genres[band.genre_id.toString()];
  let img = "/" + genre.name.toLowerCase() + ".svg";
  let band_members = getBandMembers(band.id);

  return (
    <>
    <CardHeader title={band.name} caption="" imgSrc={img} />
    <div className="sidebar-scroll">
      <div className="row">
        <div className="col col-12">
          <div className="card-text">
            <table key={"stats"+band.id} className="table">
              <thead>
                <tr><th>Rock credentials</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td>Popularity</td>
                  <td>{band.popularity}</td>
                </tr>              
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <ListOfNamedObjects title="Members" namedObjects={band_members} rowExtras={band_members.map(m => <Character size="3.5em" appearanceProps={m.appearance} />)} selectorFn="setSelectedPerson" />
    </div>
    </>
  )
}

// NOTE: BRandsSidebarContent is not to be confused with BandSideBarContent below
export function BrandsSidebarContent() {
  const apiData = useContext(ApiDataContext)
  return (
    <>
    <CardHeader title="Brands" caption={null} imgSrc={"/brand.svg"} />
    <div className="sidebar-scroll">
    <ListOfNamedObjects title={null} objectsById={apiData.brands} selectorFn="setSelectedBrand" />
    </div>
    </>
  )
}

export function BandsSidebarContent() {
  const apiData = useContext(ApiDataContext)
  return (
    <>
    <CardHeader title="Bands" caption={null} imgSrc={"/band.svg"} />
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
      <Character appearanceProps={person.appearance} />
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
              <tr><th>Measures of Rad'ness</th></tr>
            </thead>
            <tbody>
            {person.stamina > 0 &&
              <tr>
                <td>Stamina</td>
                <td>{person.stamina}</td>
              </tr> }
            {person.charisma > 0 &&
              <tr>
                <td>Charisma</td>
                <td>{person.charisma}</td>
              </tr> }             
            {person.popularity > 0 &&
              <tr>
                <td>Popularity</td>
                <td>{person.popularity}</td>
              </tr> }             
            {person.musical_talent > 0 &&
              <tr>
                <td>Musical skillz</td>
                <td>{person.musical_talent}</td>
              </tr> }                       
            {person.tech_talent > 0 &&
              <tr>
                <td>Tech wizardry</td>
                <td>{person.tech_talent}</td>
              </tr>}                        
            </tbody>
          </table>
          {person.job && 
            <table key={"job"+person.id} className="table">
              <thead>
                <tr><th>Job</th></tr>
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

const NamedObjectRow = styled.div`
  display: block;
  > * {
    display: inline-block;
  }
`

function ListOfNamedObjects({title, namedObjects, objectsById, rowExtras, selectorFn}) {
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
              {typeof namedObjects !== "undefined" &&
              namedObjects.map((obj, i) => (
                <tr key={"obj"+obj.name}>
                <td>
                <NamedObjectRow>
                {selectorFn ?
                  <a onClick={e => {
                    e.preventDefault();
                    gameFns.selectSomething({selectFn: gameFns[selectorFn], selectVal: obj});
                  }}>{obj.name}</a>
                  : obj.name
                }
                </NamedObjectRow>
                </td>
                {rowExtras && <td>{rowExtras[i]}</td>}

                </tr>
                ))}
              {typeof objectsById !== "undefined" &&
              Object.keys(objectsById).map((id, i) => (
                <tr key={"obj"+objectsById[id].name}>
                <td>
                {selectorFn ?
                  <a onClick={e => {
                    e.preventDefault();
                    gameFns.selectSomething({selectFn: gameFns[selectorFn], selectVal: objectsById[id]});
                  }}>{objectsById[id].name}</a>
                  : objectsById[id].name
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
  return (
    <>
    <CardHeader title="People" caption={null} imgSrc={"/pub.svg"} />
    <div className="sidebar-scroll">
	    <ListOfNamedObjects title="People" namedObjects={apiData.people} rowExtras={apiData.people.map(p => <Character key={p.name+"minicon"} size="2em" appearanceProps={p.appearance} />)} selectorFn="setSelectedPerson" />
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
    <CardHeader title={district.name} caption={null} imgSrc="/map.jpg" />
    <div className="sidebar-scroll">
      <PieChart percentages={percentages} colours={colours} labels={labels} />
    </div>
    </>
  )
}

function SlotBar({venue, numOfSlots, eventOptions}) {
  const gameFns = useContext(FnContext);
  let slotButtons = [...Array(numOfSlots+1).keys()].slice(1).map(function z(label) {
      let thingsInSlot = turnData.slots[venue.district_id || "0"][label].filter(event => event.venue_id === venue.id);
      return (
        <button 
          onClick={e => {
                    e.preventDefault();
                    if (thingsInSlot.length === 0) {
                      gameFns.setSelectedSlot(label)
                      if (eventOptions.length === 1) { gameFns.setSelectedEvent(eventOptions[0]) }
                    } else {
                      // TODO: Edit the event if you organised it (or something)
                      // let thingInSlot = thingsInSlot[0];
                      alert(`#TODO: Edit the event if you organised it (or something)`)
                    }
                  }}
          key={"slot"+label} type="button" className={"btn btn-secondary"}>{thingsInSlot.length ? thingsInSlot[0].kind : label}</button>
      )});

  return (
    <div className="btn-group" role="group" aria-label="Basic example" style={{width: "100%"}}>{slotButtons}</div>
  )
}

function DropDown({modelName, options, onChange, dropdownName}) {
  function setHiddenVal(inputId, value) {
    let hiddenInput = document.getElementById(inputId);
    if (hiddenInput) {
      hiddenInput.value = value;
    } 
  }
  let fieldOptions;
  if (modelName === "generic") {
    fieldOptions = options.all.map(o => (
          {
            key: o.name,
            value: o.name,
            label: o.name,
            isDisabled: (options.disabledNames.indexOf(o.name) !== -1 ? true : null)
          }))
  } else {
    fieldOptions = options.all.map(function z(o) {
      return (
          {
            key: "o"+o.id,
            value: o.id,
            label: o.name,
            isDisabled: (options.disabledIds.indexOf(o.id.toString()) !== -1 ? true : null)
          })})
  }

  return (
    <Select
      key={dropdownName}
      classNamePrefix={modelName.toLowerCase()+"Field"}
      options={fieldOptions}
      onChange={function z(e) {
        setHiddenVal(dropdownName, e.value)
        onChange && onChange(e)
      }}  />
    )
}

function EventSelectorForm({slotNumber, venue, eventTypes, eventOptions, setSelectedEvent}) {
  return (
      <DropDown
        modelName="generic"
        options={{all: venue.event_options.map(e => ({name: e.type, cost: e.requirements.money})), disabledNames: [] }}
        onChange={e => {
            setSelectedEvent(eventOptions.find(o => o.type === e.value))
            }}
      />
    )
}

function EventPlannerForm({slotNumber, venue, eventTemplate, currentMoney}) {
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)
  let bandChoices = venue.brand_id === 1 ? apiData.bands : apiData.bands.filter(band => band.brand_id === 1);
  let options = {
    "musician": {all: apiData.people.filter(person => person.job && person.job.title === "musician"),
                  disabledIds: turnData.busyPeopleIds(slotNumber)},
    "band": {all: bandChoices,
                  disabledIds: turnData.busyBandIds(slotNumber)},
  }
  // const cost = eventTemplate.requirements.money * 10;
  const [cost, setCost] = useState();
  const [bandIds, setBandIds] = useState(Array.from(document.getElementsByClassName("bandField")).map(m => m.value));
  useEffect(() => {
    if (bandChoices) {

      // function for adding two numbers. Easy!
      const add = (a, b) => a + b
      // use reduce to sum our array
      console.log("bandIds",bandIds, "bandChoices", bandChoices)
      let bandCosts = bandChoices.filter(b => bandIds.indexOf(b.id.toString()) !== -1).map(b => b.popularity * 10)
      console.log("bandcosts", bandCosts)
      bandCosts.length > 0 && setCost(bandCosts.reduce(add));
    }
  }, [bandIds]);

  return (
      <form>
        <div>Book a {eventTemplate.type}</div>
        {eventTemplate.requirements.objects.map((r, i) => (
          <div key={r.model+"-"+i} className="card">
            <div className="card-header">
              {r.model+" selector"}
            </div>
            <div className="card-body">
              <DropDown modelName={r.model} options={options[r.model.toLowerCase()]} dropdownName={r.model+"-"+i}
              onChange={function z(e) {
                
                setBandIds(Array.from(document.getElementsByClassName("bandField")).map(m => m.value));
                console.log("2",Array.from(document.getElementsByClassName("bandField")).map(m => m.value))
              }} />
              <input id={r.model+"-"+i} type="hidden" className={r.model.toLowerCase()+"Field"} />
            </div>
          </div>
        ))}
        {
          cost - currentMoney > 0 ?
            <>
            <span>£{cost}</span> <em style={{color: "red"}}>(£{cost - currentMoney} short!)</em><br/>
            <div className="btn btn-secondary">Book</div>
            </>
            :
            <>
            {cost && "£"+cost}<br/>
            <button className="btn btn-primary" onClick={e => {
                e.preventDefault();
                gameFns.selectSomething({selectFn: gameFns.setSelectedVenue, selectVal: venue});
                 
                let event = {
                  venue_id: venue.id,
                  venue_capacity: venue.stats.capacity.value,
                  venue_popularity: venue.stats.popularity.value,
                  kind: eventTemplate.type,
                  objects: {
                    "Band": [],
                    "Promoter": [],
                    "Musician": [],
                  }
                }

                eventTemplate.requirements.objects.forEach(function x(r, i) {
                  let modelName = r.model
                  let modelNameLower = modelName.toLowerCase()
                  let ids = Array.from(document.getElementsByClassName(modelNameLower+"Field")).map(m => m.value);
                  if (modelNameLower === "band") {
                    turnData.addBusyBandsIds(slotNumber, ids);
                    let musicianIds = apiData.people.filter(p => p.job && ids.indexOf(p.job.band_id.toString()) !== -1).map(p => p.id.toString());
                    turnData.addBusyPeopleIds(slotNumber, musicianIds);
                  } else {
                    turnData.addBusyPeopleIds(slotNumber, ids);
                    let bandIds = apiData.people.filter(p => ids.indexOf(p.id.toString()) !== -1 && p.job && p.job.band_id).map(p => p.job.band_id.toString())
                    turnData.addBusyBandsIds(slotNumber, bandIds);
                  }
                  event.objects[modelName] = ids
                })
                turnData.addEvent(venue.district_id || "0", slotNumber, event);
                gameFns.setCurrentMoney(currentMoney-cost)
              }
            }>Book</button>
            </>
        }

      </form>
    )
}

export function ShopSidebarContent({venue}) {
  let shop = venue;
  return (
    <>
      <CardHeader title={shop.name} caption={venue.type} imgSrc={shop.type + ".svg"} />
      <div className="sidebar-scroll">
       <Guitar />
      </div>
    </>
  )
}

export function VenueSidebarContent({venue, selectedSlot}) {
  const gameFns = useContext(FnContext)
  let eventOptions = venue.event_options;
  return (
    <>
      <CardHeader title={venue.name} caption={venue.genre_id ? gameFns.getGenre(venue.genre_id).name+" "+venue.type : venue.type} imgSrc={venue.type + ".svg"} />
      <div className="sidebar-scroll">
        <table key={"venue"+venue.id} className="table">
          <thead>
            <tr><th>Stats</th></tr>
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
        <SlotBar venue={venue} numOfSlots={venue.slots_available} eventOptions={eventOptions} setSelectedEvent={gameFns.setSelectedEvent}/>
          {selectedSlot ? <EventSelectorForm slotNumber={selectedSlot} venue={venue} eventTypes={eventOptions} eventOptions={eventOptions} setSelectedEvent={gameFns.setSelectedEvent} /> : null}
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
  const apiData = useContext(ApiDataContext)
  const gameFns = useContext(FnContext)
  const [viewport, setViewport] = useState();
  const [markers, setMarkers] = useState(null);

  useEffect(() => {
    console.log("Loading map")
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
        );
        let brandColor = venue.brand_id ? apiData.brands[venue.brand_id.toString()].colour : "rgba(0,0,0,0)"
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
              <img style={{padding: "5px", background: "radial-gradient(circle, rgba(255,255,255,1) 0%, "+brandColor+" 00%, rgba(255,255,255,0) 75%)"}} src={img} alt={venue.name}/>
            </button>
          </Marker>
        )
      }));
      console.log("Data loaded.")
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
                  // console.log(e.features[0].properties["cmwd11nm"])
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
  const [selectedBrand, setSelectedBrand] = useState();
  const [selectedBand, setSelectedBand] = useState();
  const [selectedSlot, setSelectedSlot] = useState();
  const [selectedEvent, setSelectedEvent] = useState()
  const [selectedVenue, setSelectedVenue] = useState();
  const [hoveredVenue, setHoveredVenue] = useState();
  const [selectedDistrict, setSelectedDistrict] = useState();
  const [apiData, setApiData] = useState({});
  const [currentMoney, setCurrentMoney] = useState();
  const [currentPopularity, setCurrentPopularity] = useState();

  function selectSomething({selectFn, selectVal}) {
    setSelectedTab(null);
    setSelectedPerson(null);
    setSelectedBrand(null);
    setSelectedBand(null);
    setSelectedSlot(null);
    setSelectedEvent(null);
    setSelectedVenue(null);
    setSelectedDistrict(null);
    setSelectedCity(false);
    selectFn(selectVal)
  }


  function getGenre(genreId) {
    return apiData.genres[genreId.toString()]
  }

  const gameFns = {
    "setSelectedPerson": setSelectedPerson,
    "setSelectedBrand": setSelectedBrand,
    "setSelectedBand": setSelectedBand,
    "setSelectedSlot": setSelectedSlot,
    "setSelectedEvent": setSelectedEvent,
    "setSelectedTab": setSelectedTab,
    "setSelectedCity": setSelectedCity,
    "setSelectedDistrict": setSelectedDistrict,
    "setSelectedVenue": setSelectedVenue,
    "setHoveredVenue": setHoveredVenue,
    "selectSomething": selectSomething,
    "setCurrentMoney": setCurrentMoney,
    "getGenre": getGenre,
  }

  function buildLocationEvents(data) {
    let events = {"locations": []};

    for (let i=0; i<data.locations.length; i++) {
      let e = {
        "id": data.locations[i].id, 
        "updates": {}
      }
      events.locations.push(e)
    };
    return events
  }

  function buildDistrictEvents(data) {
    let events = {"0": {"1": [], "2": [], "3": [], "4": []}};
    let districtIds = data.city.districts.map(d => d.id);
    districtIds.forEach(function z(dId) {
      events[dId] = {"1": [], "2": [], "3": [], "4": []}
    });
    let preloadedEvents = data.preloaded_events;
    if (preloadedEvents) {
      Object.keys(preloadedEvents).forEach(function z(dId) {
        events[dId] = preloadedEvents[dId]
      });
    }
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
      startTurn(data);
    }
    getData();
  }, []);

  function startTurn(data) {
    setApiData(data);
    console.log("data", data);
    setLoaded(true);
    turnData.locations = buildLocationEvents(data);
    turnData.slots = buildDistrictEvents(data);
    turnData.busyPeopleMap = {"1": [], "2": [], "3": [], "4": []};
    turnData.busyBandsMap = {"1": [], "2": [], "3": [], "4": []};
    console.log("turnData", turnData);
    setCurrentMoney(data.brands["1"].money)
    setCurrentPopularity(data.brands["1"].popularity)
  }

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
          <div className="card-body">
            {loaded && selectedCity ? <CitySidebarContent /> : null}
            {loaded && selectedVenue ? (selectedEvent && selectedSlot ?
                                        <EventPlannerForm slotNumber={selectedSlot} venue={selectedVenue} eventTemplate={selectedEvent} currentMoney={currentMoney} /> : 
                                          (selectedVenue.category === "shop" ?
                                           <ShopSidebarContent venue={selectedVenue}></ShopSidebarContent> :
                                           <VenueSidebarContent venue={selectedVenue} selectedSlot={selectedSlot}></VenueSidebarContent>) : null) : null}
        
            {loaded && selectedDistrict ? ( <DistrictSidebarContent district={selectedDistrict}></DistrictSidebarContent> ) : null}
            {loaded && selectedTab ? selectedTab : null}
            {loaded && selectedPerson ? (<PersonSidebarContent person={selectedPerson} />): null}
            {loaded && selectedBand ? (<BandSidebarContent band={selectedBand} />): null}
            {loaded && selectedBrand ? (<BrandSidebarContent brand={selectedBrand} />): null}
          </div>
          <div className="card-footer sidebar-footer text-muted">
          <div className="row">
            <div className="col col-3">
              <p className="text-left" >
                <img alt="Money: " src="/pound.svg" width="20rem" />{currentMoney}
               </p>
             </div>
             <div className="col col-3">
              <p className="text-left">
                <img alt="Popularity: " src="/popularity.svg" width="25rem" />{currentPopularity}
              </p>
            </div>
            <div className="col col-6 text-right">
              <a href="s#" className="btn btn-primary btn-sm" onClick={function() { 
                takeTurn(startTurn, buildLocationEvents, currentMoney)
                selectSomething({selectFn: setSelectedCity, selectVal: true})
              }}>Take turn</a>
            </div>
          </div>
        </div>
      </div>
    </div>
    </StatsContext.Provider>
    </FnContext.Provider>
    </ApiDataContext.Provider>
  )
}

async function takeTurn(startTurn, buildLocationEvents, currentMoney) {
  let postData = {...turnData.locationPostData, ...{events: turnData.slots}, ...{money: currentMoney}};
  console.log('Taking turn...', postData)
  let resp = await axios.post('http://localhost:8000/take_turn/', postData)
  console.log('Turn taken')
  startTurn(resp.data);
}
