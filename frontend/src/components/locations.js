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
  const locationPatterns = location.feature_patterns;

  return (
      <Foundations size={size ? size : "100%"}>
        <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 1191 842" width="1191" height="842">
          {locationPatterns.map(featurePattern => {
           return (
                <pattern id={featurePattern.name +"Pattern"} key={featurePattern.name +"Pattern"} patternUnits="userSpaceOnUse" width={featurePattern.width} height={featurePattern.height}>
                  {featurePattern.filepath && <image href={"/"+featurePattern.filepath} x="0" y="0" width={featurePattern.width} height={featurePattern.height}/>}
                </pattern>
              )}) 
          };
          
          {locationFeatures.map(feature => {
           return (
                <path id={feature.name} fill={feature.filepath === "" ? "#c35239" : ("url(#"+feature.name+"Pattern)") } stroke="#000000" strokeWidth="5" d={feature.path_d}></path>
              )}) 
          };
        </svg>
      </Foundations>
    )
};

