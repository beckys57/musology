import styled from "styled-components";
  
export const Foundations = styled.div`
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
