import React from "react";
import styled from "styled-components";
  
const Foundations = styled.div`
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

export function LocationInterior({location, size}) {
  const locationFeatures = location.features;

  return (
      <Foundations size={size ? size : "100%"}>
        <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 1191 842" width="1191" height="842">
          
          {locationFeatures.map(feature => {
            console.log("Feature,", feature)
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
      </Foundations>
    )
};

