import React from "react"
import { graphql, navigate } from "gatsby"
import styled from "@emotion/styled"

import { PostNode } from "../types"
import { GraphContainer } from "../components/graphContainer"
import { Layout } from "../components/layout"
import { InvertedShadow } from "../components/neumorphism"
import { LinkedNotes, MainNote } from "../components/note"

import "katex/dist/katex.min.css"

export default ({ data }) => {
  const note: PostNode = data.markdownRemark
  const allNotes: PostNode[] = data.allMarkdownRemark.edges.map(
    ({ node }) => node
  )

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

  const noteMap = new Map(allNotes.map(note => [note.frontmatter.uid, note]))

  const relatedNotes = [].concat(linksTo, linksFrom, [note])

  const onClickNode = nodeId => {
    if (noteMap.get(nodeId)) {
      const clickedNote = noteMap.get(nodeId)
      navigate(clickedNote.fields.slug)
    }
  }

  return (
    <Layout>
      <Grid>
        <div style={{ gridArea: "1 / 1 / 2 / 3", fontSize: "1.2em" }}>
          <MainNote note={note} externalLinks={externalLinks} />
        </div>
        <InvertedShadow style={{ gridArea: "1 / 3 / 2 / 5" }}>
          <GraphContainer
            allNotes={relatedNotes}
            onClickNode={onClickNode}
            highlightNode={note}
          />
        </InvertedShadow>
        <LinkedNotes links={allLinks} />
      </Grid>
    </Layout>
  )
}

const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-template-rows: auto;
  grid-gap: 2rem;
`

export const query = graphql`
  query($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      id
      frontmatter {
        title
        links
        uid
        categories
      }
      fields {
        slug
      }
      excerpt
    }
    allMarkdownRemark {
      edges {
        node {
          id
          html
          frontmatter {
            title
            links
            uid
            categories
          }
          fields {
            slug
          }
          excerpt
        }
      }
    }
  }
`
