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

const Hair = ({hairColor, hairDetail}) => (
    <>
      <linearGradient id="hairGradient" gradientUnits="userSpaceOnUse" x1="340.6" y1="48.89" x2="349.91" y2="606.14">
        <stop style={{stopColor: hairColor, stopOpacity: 1}} offset="0%">
        </stop>
        <stop style={{stopColor: hairDetail, stopOpacity: 1}} offset="100%">
        </stop>
      </linearGradient>
      <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill="url(#hairGradient)" fillOpacity="1" d="M531.54 127.39C582.85 181.6 545.86 226.13 545.86 254.26C545.86 293.75 544.34 405.05 541.29 588.16C447.88 510.12 382.11 471.1 343.97 471.1C230.68 471.1 145.44 532.06 145.44 412.38C145.44 374.68 116.37 221.54 132.41 190.65C148.11 160.41 123.08 80.52 168.1 52.32C213.13 24.13 297.91 37.41 340.6 37.41C427.26 37.41 480.22 73.18 531.54 127.39Z"></path>
    </>
  )


export function Character({appearanceProps}) {
  const shadeMap = {
    "#ffc999": "#e89c5d",
    "#754b32": "#56281c",
  }
  const hairGradients = {
    "1": {x1: "318.45",
          y1: "254.88",
          x2: "318.45",
          y2: "457.15"},
    "2": {x1: "340.6",
          y1: "48.8",
          x2: "349.9",
          y2: "606.1"},
    "3": {x1: "0",
          y1: "0",
          x2: "0",
          y2: "0"},
    "4": {x1: "348.05",
          y1: "18.74",
          x2: "350.86",
          y2: "220.15"},
  }
  console.log("appearanceProps", appearanceProps)
  let hairColor = appearanceProps.hair_color;
  let hairDetail = appearanceProps.hair_detail;
  let hairStyle = appearanceProps.hair_style;
  let skinDetail = shadeMap[appearanceProps.skin_color];
  let skinColor = appearanceProps.skin_color;
  let shirtColor = appearanceProps.shirt_color;
  let jacketColor = appearanceProps.jacket_color;
  let shirtDetail = appearanceProps.shirt_detail;
  let shirtStyle = appearanceProps.shirt_style;

  const hairPaths = {
    // Side bob
    "1": "M517 89.92C517 61.09 415.9 23.71 387.07 23.71C370.62 23.71 276.53 22.07 190.64 91.43C160.07 116.11 135.81 145.65 117.87 180.04C87.97 237.36 75.56 302.2 82.19 366.51C82.19 366.51 82.19 366.51 82.19 366.51C165.26 381.83 246.86 386.95 327.02 381.88C407.17 376.81 485.87 361.54 563.11 336.08C576.45 225.3 583.11 162.62 583.11 148.06C583.11 120.8 561.02 98.7 533.75 98.7C532.8 98.7 525.21 98.7 524.27 98.7C520.25 98.7 517 95.44 517 91.43C517 91.12 517 90.07 517 89.92Z",
    // Long messy
    "2": "M531.54 127.39C582.85 181.6 545.86 226.13 545.86 254.26C545.86 293.75 544.34 405.05 541.29 588.16C447.88 510.12 382.11 471.1 343.97 471.1C230.68 471.1 145.44 532.06 145.44 412.38C145.44 374.68 116.37 221.54 132.41 190.65C148.11 160.41 123.08 80.52 168.1 52.32C213.13 24.13 297.91 37.41 340.6 37.41C427.26 37.41 480.22 73.18 531.54 127.39Z",
    // Circle
    "3": "M537.87 208.92C537.87 317.8 449.47 406.2 340.6 406.2C231.72 406.2 143.32 317.8 143.32 208.92C143.32 100.05 231.72 11.65 340.6 11.65C449.47 11.65 537.87 100.05 537.87 208.92Z",
    // Mohawk
    "4": "M371.19 18.74C381.6 18.74 390.04 27.18 390.04 37.59C390.04 62.76 390.04 119.42 390.04 144.59C390.04 155 381.6 163.44 371.19 163.44C358.17 163.44 337.94 163.44 324.91 163.44C314.5 163.44 306.06 155 306.06 144.59C306.06 119.42 306.06 62.76 306.06 37.59C306.06 27.18 314.5 18.74 324.91 18.74C337.94 18.74 358.17 18.74 371.19 18.74Z",
  }
  const facePaths = {
    "1": {face: "M205.93 280.6C205.93 355.28 266.47 415.82 341.15 415.82C415.84 415.82 476.38 355.28 476.38 280.6C476.38 270.7 476.38 191.54 476.38 181.65C476.38 166.78 477.43 141.52 447.25 119.52C427.13 104.85 391.77 113.91 341.15 146.7C290.07 116.58 254.7 107.52 235.05 119.52C205.57 137.52 205.93 160.78 205.93 175.65C205.93 195.44 205.93 270.7 205.93 280.6Z",
          detail: "M417.16 122.83C428.63 122.83 442.19 171.25 442.19 184.92C442.19 194.01 442.19 266.76 442.19 275.85C442.19 339.27 402.34 391.6 350.86 399.18C355.09 399.8 359.4 400.13 363.78 400.13C421.35 400.13 468.02 344.49 468.02 275.85C468.02 266.76 468.02 171.34 468.02 162.25C468.02 148.58 444.06 122.83 432.59 122.83C427.43 122.83 419.75 122.83 417.16 122.83Z"},
    "2": {face: "M205.93 280.6C205.93 355.28 266.47 415.82 341.15 415.82C415.84 415.82 476.38 355.28 476.38 280.6C476.38 270.7 476.38 258.21 476.38 248.31C476.38 233.44 486.98 188.19 456.8 166.19C436.68 151.52 419.43 143.29 405.06 141.5C318.74 112.61 261.3 110.39 232.76 134.83C189.95 171.5 205.93 237.34 205.93 252.21C205.93 272 205.93 270.7 205.93 280.6Z",
          detail: "M426.5 160.73C437.97 160.73 442.19 209.33 442.19 220.79C442.19 228.42 442.19 289.42 442.19 297.04C442.19 350.22 402.34 394.1 350.86 400.45C355.09 400.98 359.4 401.25 363.78 401.25C421.35 401.25 468.02 354.59 468.02 297.04C468.02 289.42 468.02 209.41 468.02 201.79C468.02 190.33 446.77 167.61 437.54 163.12C428.32 158.62 429.08 160.73 426.5 160.73Z"},
    "3": {face: "M205.93 280.6C205.93 355.28 266.47 415.82 341.15 415.82C415.84 415.82 476.38 355.28 476.38 280.6C476.38 270.7 476.38 258.21 476.38 248.31C476.38 233.44 486.98 188.19 456.8 166.19C436.68 151.52 419.43 143.29 405.06 141.5C318.74 112.61 261.3 110.39 232.76 134.83C189.95 171.5 205.93 237.34 205.93 252.21C205.93 272 205.93 270.7 205.93 280.6Z",
          detail: "M426.5 160.73C437.97 160.73 442.19 209.33 442.19 220.79C442.19 228.42 442.19 289.42 442.19 297.04C442.19 350.22 402.34 394.1 350.86 400.45C355.09 400.98 359.4 401.25 363.78 401.25C421.35 401.25 468.02 354.59 468.02 297.04C468.02 289.42 468.02 209.41 468.02 201.79C468.02 190.33 446.77 167.61 437.54 163.12C428.32 158.62 429.08 160.73 426.5 160.73Z"},
    "4": {face: "M210.63 333.54C220.05 370.58 266.47 417 341.15 417C415.84 417 475.43 381.17 483.67 333.54C491.9 285.91 483.67 259.39 483.67 249.49C483.67 234.62 488.29 148.79 445.04 118.36C401.78 87.93 279.1 91.11 236.29 127.78C193.48 164.44 205.93 238.52 205.93 253.39C205.93 273.18 201.22 296.5 210.63 333.54Z", detail: "M457.59 144.17C446.62 123.88 432.04 121.33 430.03 121.33C441.5 121.33 451.6 211.48 451.6 222.99C451.6 230.64 451.6 291.9 451.6 299.55C451.6 352.96 411.75 397.01 360.27 403.4C364.5 403.92 368.81 404.2 373.19 404.2C430.76 404.2 475.07 353.77 476.24 325.39C477.42 297.01 476.78 292 476.24 284.63C474.83 265.21 473.9 257.76 473.9 252.21C473.9 240.71 475.43 204.83 465.64 170.97C463.49 163.53 460.68 149.9 457.59 144.17Z",
          detail: "M457.59 144.17C446.62 123.88 432.04 121.33 430.03 121.33C441.5 121.33 451.6 211.48 451.6 222.99C451.6 230.64 451.6 291.9 451.6 299.55C451.6 352.96 411.75 397.01 360.27 403.4C364.5 403.92 368.81 404.2 373.19 404.2C430.76 404.2 475.07 353.77 476.24 325.39C477.42 297.01 476.78 292 476.24 284.63C474.83 265.21 473.9 257.76 473.9 252.21C473.9 240.71 475.43 204.83 465.64 170.97C463.49 163.53 460.68 149.9 457.59 144.17Z",
          onTop: true},
  }

  const shirtPaths = {
    "1": {shirt: "M244.76 448.82L341.15 486.16L437.54 448.82L437.54 672.01L244.76 672.01L244.76 448.82Z",
          detail: "M405.06 588.16C405.06 622.57 376.43 650.5 341.15 650.5C305.88 650.5 277.25 622.57 277.25 588.16C277.25 553.76 305.88 525.83 341.15 525.83C376.43 525.83 405.06 553.76 405.06 588.16Z",
          jacketPaths: ["M283.23 439.82L283.23 525.83L295.23 672.33L211.46 672.33L211.46 633.15L205.93 600.32C197.68 501.58 193.47 452.01 193.3 451.6C190.25 444.06 217.95 439.82 226.1 439.82C239.09 439.82 258.13 439.82 283.23 439.82Z", "M491.15 499.99L470.85 632.83L470.85 672.01L387.07 672.01L395.07 531.83L399.07 445.15C449.54 444.93 478.01 444.82 484.51 444.82C489.94 444.82 493.48 450.09 495.15 460.61L491.15 499.99Z"]},
    "2": {shirt: "M236.29 588.16L175.14 546.54C171.59 546.68 170.25 533.49 171.14 506.96C172.48 467.16 188.07 452.66 198.17 445.15C204.89 440.15 222.94 437.37 252.29 436.82C280.42 469.71 309.89 486.16 340.68 486.16C371.48 486.16 398.28 471.15 421.07 441.15C454.51 439.07 474.51 440.41 481.08 445.15C490.94 452.27 506.66 474.24 508.5 506.96C510.34 539.67 511.44 536.15 508.5 546.54C505.18 558.27 484.04 572.14 445.07 588.16L445.07 672.01C332.12 672.01 261.52 672.01 233.28 672.01C233.11 672.01 232.97 671.86 232.97 671.68C233.41 660.55 234.52 632.71 236.29 588.16Z",
          detail: "M429.41 448.52C415.09 466.59 397.37 480.25 376.25 489.51C355.13 498.78 331.73 498.78 306.06 489.51C273.59 537.95 253.3 568.22 245.18 580.33C244.6 581.19 244.29 582.2 244.29 583.24C244.29 593.66 244.29 619.72 244.29 661.42L465.64 448.52L429.41 448.52Z"},
  }
  return (
      <Frame>
        <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 681 681" width="681" height="681">
          <linearGradient id="hairGradient" gradientUnits="userSpaceOnUse" x1={hairGradients[hairStyle].x1} y1={hairGradients[hairStyle].y1} x2={hairGradients[hairStyle].x2} y2={hairGradients[hairStyle].y2}>
            <stop style={{stopColor: hairColor, stopOpacity: 1}} offset="0%">
            </stop>
            <stop style={{stopColor: hairDetail, stopOpacity: 1}} offset="100%">
            </stop>
          </linearGradient>
          {!facePaths[hairStyle].onTop && <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill="url(#hairGradient)" fillOpacity="1" d={hairPaths[hairStyle]}></path>}
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M524.46 672.01L157.85 672.01L189.61 466.66C189.97 464.35 190.17 463.07 190.21 462.82C191.81 452.45 200.73 444.82 211.21 444.82C216.81 444.82 241.26 443.15 284.57 439.82L295.23 363.24L387.08 363.24L399.07 444.82C441.49 444.82 465.51 444.82 471.11 444.82C481.59 444.82 490.5 452.45 492.11 462.82C492.15 463.07 492.34 464.35 492.7 466.66L524.46 672.01Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill={skinDetail} fillOpacity="1" d="M488.28 465.64C488.02 463.44 487.88 462.22 487.85 461.98C486.67 452.1 480.11 444.82 472.4 444.82C470.31 444.82 453.56 444.82 451.47 444.82C459.17 444.82 465.74 452.1 466.91 461.98C466.94 462.22 467.09 463.44 467.35 465.64L490.72 661.42L511.64 661.42L488.28 465.64Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M449.54 240.9L449.54 313.49C476.61 313.49 491.65 313.49 494.66 313.49C507.44 313.49 517.8 303.13 517.8 290.36C517.8 287.72 517.8 266.66 517.8 264.03C517.8 251.25 507.44 240.9 494.66 240.9C488.64 240.9 473.6 240.9 449.54 240.9Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d="M232.76 240.9L232.76 313.49C205.7 313.49 190.66 313.49 187.65 313.49C174.87 313.49 164.51 303.13 164.51 290.36C164.51 287.72 164.51 266.66 164.51 264.03C164.51 251.25 174.87 240.9 187.65 240.9C193.67 240.9 208.7 240.9 232.76 240.9Z"></path>
          <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={shirtColor} fillOpacity="1" d={shirtPaths[shirtStyle].shirt}></path>
          <path stroke="#000000" strokeWidth="10" strokeOpacity="1" fill={shirtDetail} fillOpacity="1" d={shirtPaths[shirtStyle].detail}></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill={skinDetail} fillOpacity="1" d="M295.23 431.51C305.7 436.62 316.92 440.42 328.69 442.69C337.04 444.31 345.65 445.15 354.47 445.15C365.72 445.15 376.63 443.77 387.07 441.18C387.07 435.99 387.07 410.01 387.07 363.24L295.23 363.24C295.23 399.65 295.23 422.41 295.23 431.51Z"></path>
          <path id="face" stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={skinColor} fillOpacity="1" d={facePaths[hairStyle].face}></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill="#000000" fillOpacity="1" d={"M373.68 329.12C377.37 325.02 377.04 318.71 372.94 315.02C368.85 311.32 362.53 311.65 358.84 315.75C353.99 321.13 347.71 324.1 341.16 324.1C334.6 324.1 328.32 321.13 323.48 315.75C319.78 311.65 313.46 311.32 309.36 315.02C305.26 318.71 304.94 325.03 308.63 329.12C317.31 338.77 328.87 344.08 341.16 344.08C353.45 344.08 364.99 338.77 373.68 329.12Z"}></path>
          <path id="faceDetail" stroke="#000000" strokeWidth="1" strokeOpacity="0" fill={skinDetail} fillOpacity="1" d={facePaths[hairStyle].detail}></path>
          {facePaths[hairStyle].onTop && <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill="url(#hairGradient)" fillOpacity="1" d={hairPaths[hairStyle]}></path>}
          {shirtPaths[shirtStyle].jacketPaths && shirtPaths[shirtStyle].jacketPaths.map(jPath => <path stroke="#000000" strokeWidth="20" strokeOpacity="1" fill={jacketColor} fillOpacity="1" d={jPath}></path>)}
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill="#000000" fillOpacity="1" d="M287.24 254.28C287.24 253.87 287.24 250.56 287.24 250.14C287.24 244.63 282.77 240.15 277.24 240.15C271.73 240.15 267.25 244.63 267.25 250.14C267.25 250.56 267.25 253.87 267.25 254.28C267.25 259.8 271.73 264.27 277.24 264.27C282.77 264.27 287.24 259.8 287.24 254.28Z"></path>
          <path stroke="#000000" strokeWidth="1" strokeOpacity="0" fill="#000000" fillOpacity="1" d="M415.05 250.14C415.05 244.63 410.58 240.15 405.06 240.15C399.55 240.15 395.07 244.63 395.07 250.14C395.07 250.56 395.07 253.87 395.07 254.28C395.07 259.8 399.55 264.27 405.06 264.27C410.58 264.27 415.05 259.8 415.05 254.28C415.05 253.45 415.05 250.56 415.05 250.14Z"></path>
        </svg>
      </Frame>
    )
};
