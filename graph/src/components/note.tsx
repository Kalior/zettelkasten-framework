import React from "react"
import { Link } from "gatsby"
import styled from "@emotion/styled"
import { Helmet } from "react-helmet"

import { PostNode } from "../types"
import { CategoryList } from "../components/categoryList"
import { InvertedShadow, Shadow } from "./neumorphism"

interface NoteProps {
  note: PostNode
  allNotes: PostNode[]
}

export const Note: React.FC<NoteProps> = ({ note, allNotes }) => {
  const linksTo = allNotes.filter(
    node =>
      node.id != note.id &&
      node.frontmatter.links.some(link => link == note.frontmatter.uid)
  )
  const linksFrom = allNotes.filter(
    node =>
      node.id != note.id &&
      note.frontmatter.links.some(link => link == node.frontmatter.uid)
  )
  const allLinks = [...new Set([].concat(linksTo, linksFrom))]

  const externalLinks = note.frontmatter.links.filter(
    link => !allNotes.some(node => link == node.frontmatter.uid)
  )

  return (
    <Container>
      <div style={{ marginBottom: "2em" }}>
        <MainNote note={note} externalLinks={externalLinks} />
      </div>
      <Grid>
        <LinkedNotes links={allLinks} />
      </Grid>
    </Container>
  )
}

const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-template-rows: auto;
  grid-gap: 1rem;
`

export const MainNote = ({ note, externalLinks }) => (
  <>
    <NoteContainer note={note} />
    {externalLinks.length != 0 && <h2>Sources</h2>}
    <ul>
      {externalLinks.map(link => (
        <li key={link}>
          <ExternalLink href={link}>{link}</ExternalLink>
        </li>
      ))}
    </ul>
  </>
)

export const LinkedNotes = ({ links }) => (
  <>
    {links.map(node => (
      <div key={node.id} style={{ fontSize: "0.8em" }}>
        <NoteContainerWithShadow note={node} />
      </div>
    ))}
  </>
)

const ExternalLink = styled.a`
  display: block;
  text-decoration: none;
  color: inherit;

  margin-bottom: 0.4em;

  :hover {
    text-decoration: underline;
  }
`

interface NoteContainerProps {
  note: PostNode
}

export const NoteContainerWithShadow: React.FC<NoteContainerProps> = ({
  note,
}) => (
  <div>
    <Shadow style={{ padding: "2em" }}>
      <NoteContainer note={note} />
    </Shadow>
  </div>
)

export const NoteContainer: React.FC<NoteContainerProps> = ({ note }) => (
  <NoteDiv>
    <CategoryList categories={note.frontmatter.categories} />
    <LinkCard to={note.fields.slug}>
      <Helmet>
        <script
          src="https://cdn.jsdelivr.net/npm/mathjax@3.0.1/es5/tex-mml-chtml.js"
          async
        ></script>
      </Helmet>
      <h2>{note.frontmatter.title}</h2>
      <div dangerouslySetInnerHTML={{ __html: note.html }} />
    </LinkCard>
  </NoteDiv>
)

const NoteDiv = styled.div`
  max-width: 30em;
`

const Container = styled.div`
  display: flex;
  flex-flow: column;
`

const LinkCard = styled(Link)`
  display: block;

  cursor: pointer;
  text-decoration: none;
  color: inherit;

  :hover {
    text-decoration: underline;
  }
`
