import React from "react";
import styled from "styled-components";

const Case = styled.div`
  position: relative;
  height: 10em;
  width: auto;
  & img {
    position: absolute;
    height: 100%;
    width: auto;
  }
`

export function Guitar() {
  return (
      <Case>
        <img alt="guitar body" src="guitar-body.svg" />
        <img alt="guitar neck" src="guitar-neck.svg" />
        <img alt="guitar head" src="guitar-head.svg" />
      </Case>
    )
};
