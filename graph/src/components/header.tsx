import React from "react"
import { Link } from "gatsby"
import styled from "@emotion/styled"

export default () => (
  <Header>
    <h1
      style={{
        margin: "1rem",
        fontWeight: 500,
        fontSize: "1.2em",
        display: "inline-block",
        borderBottom: "1px solid",
      }}
    >
      Zettelkasten
    </h1>
    <StyledLink style={{ margin: "1rem" }} to="/">
      All notes
    </StyledLink>
    <StyledLink style={{ margin: "1rem" }} to="/graph">
      Full graph
    </StyledLink>
  </Header>
)

const Header = styled.div`
  padding: 1rem;
`

const StyledLink = styled(Link)`
  color: inherit;
  text-decoration: none;
  :hover {
    text-decoration: underline;
  }
`
