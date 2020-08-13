import React, { useContext, useEffect, useState } from "react";
import styled from "styled-components";
import axios from "axios"
import {FnContext} from "../App.js"
import {Foundations} from "./locations.js"
  
const SVGContainer = styled.div`
  position: relative;
  width: "74vw";
  height: "100%";
  & img {
    position: absolute;
    height: 100%;
    width: auto;
  }
  & svg {
    position: absolute;
    width: 100%;
    height: auto;

  }
  ${props => props.size && `
    width: ${props.size};
  `}
`

export function ItemSVG({items, size}) {
  return (
          <SVGContainer size={size ? size : "100%"}>
            <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 1191 842" width="1191" height="842">
              {items.map(feature => {
               return (
                 <>
                    <pattern id={"patternF" + feature.id} key={"patternF" + feature.id} patternUnits="userSpaceOnUse" width={feature.width} height={feature.height} x={feature.x} y={feature.y}>
                      {feature.filepath && <image href={"/"+feature.filepath} width={feature.width} height={feature.height}/>}
                    </pattern>
                    <path id={feature.category} fill={feature.filepath === "" ? "#c35239" : ("url(#"+"patternF"+feature.id + ")") } stroke="#000000" strokeWidth={feature.has_border? "0" : "5"} d={feature.path_d}></path>
                 </>
                 )}) 
              };
            </svg>
          </SVGContainer>
   )
};

export function Catalogue({venue}) {
  const [loaded, setLoaded] = useState(false);
  const [items, setItems] = useState();

  async function getCatalogue(venue_id) {
    console.log('Fetching catalogue...', venue_id)
    let resp = await axios.get('http://localhost:8000/catalogue/location/'+venue_id+'/')
    console.log('Got it', resp.data)
    setItems(resp.data);
    setLoaded(true);
  }

  useEffect(() => {
    !loaded && getCatalogue(venue.id);
  }, [venue, items, loaded]);

  return (items ? <ItemSVG items={items} /> : <h1>Loading</h1>)
};

