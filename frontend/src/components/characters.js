import React from "react";
import styled from "styled-components";

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
`

const Hair = ({hairStyle, hairColor, hairDetail}) => {
  const hairGradients = {
    "1": {x1: "318.45",
          y1: "254.88",
          x2: "318.45",
          y2: "457.15"},
    "2": {x1: "340.6",
          y1: "48.8",
          x2: "349.9",
          y2: "606.1"},
  }
  console.log("hairStyle", hairGradients[hairStyle].x1)

  const paths = {
    "1": "M449.54 240.9L449.54 313.49C476.61 313.49 491.65 313.49 494.66 313.49C507.44 313.49 517.8 303.13 517.8 290.36C517.8 287.72 517.8 266.66 517.8 264.03C517.8 251.25 507.44 240.9 494.66 240.9C488.64 240.9 473.6 240.9 449.54 240.9Z",
    "2": "M531.54 127.39C582.85 181.6 545.86 226.13 545.86 254.26C545.86 293.75 544.34 405.05 541.29 588.16C447.88 510.12 382.11 471.1 343.97 471.1C230.68 471.1 145.44 532.06 145.44 412.38C145.44 374.68 116.37 221.54 132.41 190.65C148.11 160.41 123.08 80.52 168.1 52.32C213.13 24.13 297.91 37.41 340.6 37.41C427.26 37.41 480.22 73.18 531.54 127.39Z",
  }

  let pathD = paths[hairStyle];
  console.log("path", pathD)
  let tid = "gradientHair"+hairStyle

  return (
      <>
        <linearGradient id="gradientHair" gradientUnits="userSpaceOnUse" x1={hairGradients[hairStyle].x1} y1={hairGradients[hairStyle].y1} x2={hairGradients[hairStyle].x2} y2={hairGradients[hairStyle].y2}>
          <stop style={{stopColor: hairColor, stopOpacity: 1}} offset="0%"></stop>
          <stop style={{stopColor: hairDetail, stopOpacity: 1}} offset="100%"></stop>
        </linearGradient>
        <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={"url(#gradientHair)"} fillOpacity="1" d="M449.54 240.9L449.54 313.49C476.61 313.49 491.65 313.49 494.66 313.49C507.44 313.49 517.8 303.13 517.8 290.36C517.8 287.72 517.8 266.66 517.8 264.03C517.8 251.25 507.44 240.9 494.66 240.9C488.64 240.9 473.6 240.9 449.54 240.9Z"></path>
      </>
  )
}


export function Character({appearanceProps}) {
  const shadeMap = {
    "#ffc999": "#e89c5d",
    "#754b32": "#56281c",
  }
  let hairColor = appearanceProps.hair_color;
  let hairDetail = appearanceProps.hair_detail;
  let hairStyle = appearanceProps.hair_style;
  let skinDetail = shadeMap[appearanceProps.skin_color];
  let skinColor = appearanceProps.skin_color;
  let shirtColor = appearanceProps.shirt_color;
  let shirtDetail = appearanceProps.shirt_detail;

  return (
      <Frame>
        <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 681 681" width="681" height="681">
        <Hair hairStyle={hairStyle} hairColor={hairColor} hairDetail={hairDetail} />
        <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M524.46 672.01L157.85 672.01L189.61 466.66C189.97 464.35 190.17 463.07 190.21 462.82C191.81 452.45 200.73 444.82 211.21 444.82C216.81 444.82 241.26 443.15 284.57 439.82L295.23 363.24L387.08 363.24L399.07 444.82C441.49 444.82 465.51 444.82 471.11 444.82C481.59 444.82 490.5 452.45 492.11 462.82C492.15 463.07 492.34 464.35 492.7 466.66L524.46 672.01Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill={skinDetail} fillOpacity="1" d="M488.28 465.64C488.02 463.44 487.88 462.22 487.85 461.98C486.67 452.1 480.11 444.82 472.4 444.82C470.31 444.82 453.56 444.82 451.47 444.82C459.17 444.82 465.74 452.1 466.91 461.98C466.94 462.22 467.09 463.44 467.35 465.64L490.72 661.42L511.64 661.42L488.28 465.64Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M449.54 240.9L449.54 313.49C476.61 313.49 491.65 313.49 494.66 313.49C507.44 313.49 517.8 303.13 517.8 290.36C517.8 287.72 517.8 266.66 517.8 264.03C517.8 251.25 507.44 240.9 494.66 240.9C488.64 240.9 473.6 240.9 449.54 240.9Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M232.76 240.9L232.76 313.49C205.7 313.49 190.66 313.49 187.65 313.49C174.87 313.49 164.51 303.13 164.51 290.36C164.51 287.72 164.51 266.66 164.51 264.03C164.51 251.25 174.87 240.9 187.65 240.9C193.67 240.9 208.7 240.9 232.76 240.9Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill={skinDetail} fillOpacity="1" d="M295.23 431.51C305.7 436.62 316.92 440.42 328.69 442.69C337.04 444.31 345.65 445.15 354.47 445.15C365.72 445.15 376.63 443.77 387.07 441.18C387.07 435.99 387.07 410.01 387.07 363.24L295.23 363.24C295.23 399.65 295.23 422.41 295.23 431.51Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={shirtColor} fillOpacity="1" d="M236.29 588.16L175.14 546.54C171.59 546.68 170.25 533.49 171.14 506.96C172.48 467.16 188.07 452.66 198.17 445.15C204.89 440.15 222.94 437.37 252.29 436.82C280.42 469.71 309.89 486.16 340.68 486.16C371.48 486.16 398.28 471.15 421.07 441.15C454.51 439.07 474.51 440.41 481.08 445.15C490.94 452.27 506.66 474.24 508.5 506.96C510.34 539.67 511.44 536.15 508.5 546.54C505.18 558.27 484.04 572.14 445.07 588.16L445.07 672.01C332.12 672.01 261.52 672.01 233.28 672.01C233.11 672.01 232.97 671.86 232.97 671.68C233.41 660.55 234.52 632.71 236.29 588.16Z"></path>
          <path stroke="#000000" strokeWidth="10" strokeOpacity="1" fill={shirtDetail} fillOpacity="1" d="M429.41 448.52C415.09 466.59 397.37 480.25 376.25 489.51C355.13 498.78 331.73 498.78 306.06 489.51C273.59 537.95 253.3 568.22 245.18 580.33C244.6 581.19 244.29 582.2 244.29 583.24C244.29 593.66 244.29 619.72 244.29 661.42L465.64 448.52L429.41 448.52Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M205.93 280.6C205.93 355.28 266.47 415.82 341.15 415.82C415.84 415.82 476.38 355.28 476.38 280.6C476.38 270.7 476.38 258.21 476.38 248.31C476.38 233.44 486.98 188.19 456.8 166.19C436.68 151.52 419.43 143.29 405.06 141.5C318.74 112.61 261.3 110.39 232.76 134.83C189.95 171.5 205.93 237.34 205.93 252.21C205.93 272 205.93 270.7 205.93 280.6Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill="#000000" fillOpacity="1" d="M373.68 329.12C377.37 325.02 377.04 318.71 372.94 315.02C368.85 311.32 362.53 311.65 358.84 315.75C353.99 321.13 347.71 324.1 341.16 324.1C334.6 324.1 328.32 321.13 323.48 315.75C319.78 311.65 313.46 311.32 309.36 315.02C305.26 318.71 304.94 325.03 308.63 329.12C317.31 338.77 328.87 344.08 341.16 344.08C353.45 344.08 364.99 338.77 373.68 329.12Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill={skinDetail} fillOpacity="1" d="M426.5 160.73C437.97 160.73 442.19 209.33 442.19 220.79C442.19 228.42 442.19 289.42 442.19 297.04C442.19 350.22 402.34 394.1 350.86 400.45C355.09 400.98 359.4 401.25 363.78 401.25C421.35 401.25 468.02 354.59 468.02 297.04C468.02 289.42 468.02 209.41 468.02 201.79C468.02 190.33 446.77 167.61 437.54 163.12C428.32 158.62 429.08 160.73 426.5 160.73Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill="#000000" fillOpacity="1" d="M287.24 254.28C287.24 253.87 287.24 250.56 287.24 250.14C287.24 244.63 282.77 240.15 277.24 240.15C271.73 240.15 267.25 244.63 267.25 250.14C267.25 250.56 267.25 253.87 267.25 254.28C267.25 259.8 271.73 264.27 277.24 264.27C282.77 264.27 287.24 259.8 287.24 254.28Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill="#000000" fillOpacity="1" d="M415.05 250.14C415.05 244.63 410.58 240.15 405.06 240.15C399.55 240.15 395.07 244.63 395.07 250.14C395.07 250.56 395.07 253.87 395.07 254.28C395.07 259.8 399.55 264.27 405.06 264.27C410.58 264.27 415.05 259.8 415.05 254.28C415.05 253.45 415.05 250.56 415.05 250.14Z"></path>
        </svg>
      </Frame>
    )
};
