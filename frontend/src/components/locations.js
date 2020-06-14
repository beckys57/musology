import React from "react";
import styled from "styled-components";

const Foundations = styled.div`
  position: relative;
  height: auto;
  width: 100%;
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