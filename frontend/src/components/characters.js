import React from "react";
import styled from "styled-components";
import {shadeMap, hairPaths, facePaths, jacketPaths, shirtPaths, mouthPaths, hairGradients} from "./svg_data/characters"

const Frame = styled.div`
  position: relative;
  height: 5em;
  width: auto;
  & img {
    position: absolute;
    height: 100%;
    width: auto;
  }
  & svg {
    width: auto;
    height: 100%;

  }
  ${props => props.size && `
    height: ${props.size};
  `}
`

function getMouthPath(appearanceProps) {
  let mouthPath;
  switch(appearanceProps.happiness) {
    case '0':
    case '1':
    case '2':
      // code block
      mouthPath = mouthPaths["sad"]
      break;
    case '3':
    case '4':
      // code block
      mouthPath = mouthPaths["fairly_sad"]
      break;
    case '5':
    case '6':
      // code block
      mouthPath = mouthPaths["neutral"]
      break;
    case '7':
    case '8':
      // code block
      mouthPath = mouthPaths["fairly_happy"]
      break;
    default:
      // code block
      mouthPath = mouthPaths["happy"]
  } 
  return mouthPath;
}

export function Character({appearanceProps, size}) {
  let hairColor = appearanceProps.hair_color;
  let hairDetail = appearanceProps.hair_detail;
  let hairStyle = appearanceProps.hair_style;
  let skinDetail = shadeMap[appearanceProps.skin_color];
  let skinColor = appearanceProps.skin_color;
  let shirtColor = appearanceProps.shirt_color;
  let jacketStyle = appearanceProps.jacket_style;
  let jacketColor = appearanceProps.jacket_color;
  let shirtDetail = appearanceProps.shirt_detail;
  let shirtStyle = appearanceProps.shirt_style;
 
  let mouthPath = getMouthPath(appearanceProps);

  return (
      <Frame size={size ? size : "5em"}>
        <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 681 681" width="681" height="681">
          {hairGradients[hairStyle] && <linearGradient id={"hairGradient-"+hairColor+hairDetail} gradientUnits="userSpaceOnUse" x1={hairGradients[hairStyle].x1} y1={hairGradients[hairStyle].y1} x2={hairGradients[hairStyle].x2} y2={hairGradients[hairStyle].y2}>
            <stop style={{stopColor: hairColor, stopOpacity: 1}} offset="0%">
            </stop>
            <stop style={{stopColor: hairDetail, stopOpacity: 1}} offset="100%">
            </stop>
          </linearGradient>}
          {!facePaths[hairStyle].onTop && <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={hairGradients[hairStyle] ? "url(#hairGradient-"+hairColor+hairDetail+")" : hairColor} fillOpacity="1" d={hairPaths[hairStyle]}></path>}
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M524.46 672.01L157.85 672.01L189.61 466.66C189.97 464.35 190.17 463.07 190.21 462.82C191.81 452.45 200.73 444.82 211.21 444.82C216.81 444.82 241.26 443.15 284.57 439.82L295.23 363.24L387.08 363.24L399.07 444.82C441.49 444.82 465.51 444.82 471.11 444.82C481.59 444.82 490.5 452.45 492.11 462.82C492.15 463.07 492.34 464.35 492.7 466.66L524.46 672.01Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill={skinDetail} fillOpacity="1" d="M488.28 465.64C488.02 463.44 487.88 462.22 487.85 461.98C486.67 452.1 480.11 444.82 472.4 444.82C470.31 444.82 453.56 444.82 451.47 444.82C459.17 444.82 465.74 452.1 466.91 461.98C466.94 462.22 467.09 463.44 467.35 465.64L490.72 661.42L511.64 661.42L488.28 465.64Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M449.54 240.9L449.54 313.49C476.61 313.49 491.65 313.49 494.66 313.49C507.44 313.49 517.8 303.13 517.8 290.36C517.8 287.72 517.8 266.66 517.8 264.03C517.8 251.25 507.44 240.9 494.66 240.9C488.64 240.9 473.6 240.9 449.54 240.9Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M232.76 240.9L232.76 313.49C205.7 313.49 190.66 313.49 187.65 313.49C174.87 313.49 164.51 303.13 164.51 290.36C164.51 287.72 164.51 266.66 164.51 264.03C164.51 251.25 174.87 240.9 187.65 240.9C193.67 240.9 208.7 240.9 232.76 240.9Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill={skinDetail} fillOpacity="1" d="M295.23 431.51C305.7 436.62 316.92 440.42 328.69 442.69C337.04 444.31 345.65 445.15 354.47 445.15C365.72 445.15 376.63 443.77 387.07 441.18C387.07 435.99 387.07 410.01 387.07 363.24L295.23 363.24C295.23 399.65 295.23 422.41 295.23 431.51Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={shirtColor} fillOpacity="1" d={shirtPaths[shirtStyle].shirt}></path>
          {!shirtPaths[shirtStyle].detailOnTop && <path stroke="#000000" strokeWidth="15" strokeOpacity="1" fill={shirtDetail} fillOpacity="1" d={shirtPaths[shirtStyle].detail}></path>}
          {jacketPaths[jacketStyle] && jacketPaths[jacketStyle].map((jPath, i) => <path key={"jacketPath"+i} stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={jacketColor} fillOpacity="1" d={jPath}></path>)}
          {shirtPaths[shirtStyle].detailOnTop && <path stroke="#000000" strokeWidth="15" strokeOpacity="1" fill={shirtDetail} fillOpacity="1" d={shirtPaths[shirtStyle].detail}></path>}
          <path id="face" stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d={facePaths[hairStyle].face}></path>
          <path id="faceDetail" stroke="#000000" strokeWidth="1" strokeOpacity="0" fill={skinDetail} fillOpacity="1" d={facePaths[hairStyle].detail}></path>
          <path id="mouth" stroke="#000000" strokeWidth="1" strokeOpacity="0" fill="#000000" fillOpacity="1" d={mouthPath}></path>
          {facePaths[hairStyle].onTop && <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={"url(#hairGradient-"+hairColor+hairDetail+")"} fillOpacity="1" d={hairPaths[hairStyle]}></path>}
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill="#000000" fillOpacity="1" d="M287.24 254.28C287.24 253.87 287.24 250.56 287.24 250.14C287.24 244.63 282.77 240.15 277.24 240.15C271.73 240.15 267.25 244.63 267.25 250.14C267.25 250.56 267.25 253.87 267.25 254.28C267.25 259.8 271.73 264.27 277.24 264.27C282.77 264.27 287.24 259.8 287.24 254.28Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill="#000000" fillOpacity="1" d="M415.05 250.14C415.05 244.63 410.58 240.15 405.06 240.15C399.55 240.15 395.07 244.63 395.07 250.14C395.07 250.56 395.07 253.87 395.07 254.28C395.07 259.8 399.55 264.27 405.06 264.27C410.58 264.27 415.05 259.8 415.05 254.28C415.05 253.45 415.05 250.56 415.05 250.14Z"></path>
        </svg>
      </Frame>
    )
};
