import React, { useState } from "react"
import { graphql } from "gatsby"
import { PostNode } from "../types"

import { Note } from "../components/note"
import { GraphContainer } from "../components/graphContainer"
import { Layout } from "../components/layout"
import { InvertedShadow } from "../components/neumorphism"

export default ({ data }) => {
  const allNotes: PostNode[] = data.allMarkdownRemark.edges.map(
    ({ node }) => node
  )

  const noteMap = new Map(allNotes.map(note => [note.frontmatter.uid, note]))

  const [note, setNote] = useState(allNotes[0])

  const onClickNode = nodeId => {
    if (noteMap.get(nodeId)) {
      setNote(noteMap.get(nodeId))
    }
  }

  return (
    <Layout>
      <InvertedShadow style={{ marginBottom: "2rem" }}>
        <GraphContainer
          allNotes={allNotes}
          onClickNode={onClickNode}
          width={1800}
        />
      </InvertedShadow>
      <Note note={note} allNotes={allNotes} />
    </Layout>
  )
}

export const query = graphql`
  query {
    allMarkdownRemark {
      edges {
        node {
          id
          html
          frontmatter {
            uid
            title
            date
            links
            categories
          }
          fields {
            slug
          }
        }
      }
    }
  }
`
