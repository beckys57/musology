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
  return (
      <Foundations size={size ? size : "100%"}>
        <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 1191 842" width="1191" height="842">
          <pattern id="floorPattern" patternUnits="userSpaceOnUse" width="15" height="15">
            <image href="/Carbon-Fibre.svg" x="0" y="0" width="15" height="15"/>
          </pattern>
          <pattern id="wallPattern" patternUnits="userSpaceOnUse" width="100" height="100">
            <image href="/Protruding-Squares-Wallpaper.svg" x="0" y="0" width="100" height="100" />
          </pattern>
          <pattern id="wallObject" patternUnits="userSpaceOnUse" width="56" height="100">
            <image href="/Honeycomb-Art.svg" x="0" y="0" width="56" height="100"/>
          </pattern>
          <pattern id="barPattern" patternUnits="userSpaceOnUse" width="100" height="100">
            <image href="/wood.svg" x="0" y="0" width="100" height="100"/>
          </pattern>
          <path id="floor" fill="url(#floorPattern)" stroke="#000000" strokeWidth="5" d="M0 278.91L1191 278.91L1191 842L0 842L0 278.91Z"></path>
          <path id="wall" fill="url(#wallPattern)" stroke="#000000" strokeWidth="5" d="M0 -2.64L1191 -2.64L1191 278.91L0 278.91L0 -2.64Z"></path>
          <path id="bar" fill="url(#barPattern)" stroke="#000000" strokeWidth="5" d="M0 212.67L595.5 212.67L595.5 354.33L0 354.33L0 212.67Z"></path>
          <path id="wallObj" fill="#f3ff03" stroke="#000000" strokeWidth="5" d="M640.92 82.66L751.33 82.66L751.33 222.24L640.92 222.24L640.92 82.66Z"></path>
          <path id="wallObj" fill="url(#wallObject)" stroke="#000000" strokeWidth="5" d="M792.72 33.07L903.14 33.07L903.14 172.66L792.72 172.66L792.72 33.07Z"></path>
          <path id="wallObj" fill="#f3ff03" stroke="#000000" strokeWidth="5" d="M937.17 101.82L1047.58 101.82L1047.58 241.41L937.17 241.41L937.17 101.82Z"></path>
          <path id="barStool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M64.25 262.41L126.75 262.41L126.75 401.99L64.25 401.99L64.25 262.41Z"></path>
          <path id="barStool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M168.14 262.41L230.64 262.41L230.64 401.99L168.14 401.99L168.14 262.41Z"></path>
          <path id="barStool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M270.22 262.41L332.72 262.41L332.72 401.99L270.22 401.99L270.22 262.41Z"></path>
          <path id="barStool" fill="#c35239" stroke="#000000" strokeWidth="5" d="M374.1 262.41L436.6 262.41L436.6 401.99L374.1 401.99L374.1 262.41Z"></path>
          <path id="drinksCabinet" fill="#bc25b3" stroke="#000000" strokeWidth="5" d="M0 30.99L595.5 30.99L595.5 172.66L0 172.66L0 30.99Z"></path>
          <path id="barLighting" fill="#2d3879" stroke="#000000" strokeWidth="5" d="M0 0L595.5 0L595.5 30.99L0 30.99L0 0Z"></path>
          <path id="stage" fill="#662078" stroke="#000000" strokeWidth="5" d="M563.92 554.5L1191 554.5L1191 842L563.92 842L563.92 554.5Z"></path>
          <path id="soundSystem" fill="#c61f1d" stroke="#000000" strokeWidth="5" d="M937.17 362.24L1076.75 362.24L1076.75 554.5L937.17 554.5L937.17 362.24Z"></path>
          <path id="stageTop" fill="#f54207" stroke="#000000" strokeWidth="5" d="M687.88 -1.17L1191 -1.17L1191 101.82L687.88 101.82L687.88 -1.17Z"></path>
          <path id="stageBack" fill="#f54207" stroke="#000000" strokeWidth="5" d="M1088.01 101.82L1191 101.82L1191 842L1088.01 842L1088.01 101.82Z"></path>
          <path id="stageBottom" fill="#f54207" stroke="#000000" strokeWidth="5" d="M563.92 739.01L1191 739.01L1191 842L563.92 842L563.92 739.01Z"></path>
          <path id="danceFloor" fill="#e881ec" stroke="#000000" strokeWidth="5" d="M0 739.01L563.92 739.01L563.92 842L0 842L0 739.01Z"></path>
        </svg>
      </Foundations>
    )
};

