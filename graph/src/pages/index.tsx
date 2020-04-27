import React from "react"
import { graphql } from "gatsby"

import { Layout } from "../components/layout"

import { NoteField } from "../components/noteField"

export default ({ data }) => {
  return (
    <Layout>
      <div>
        <h4>{data.allMarkdownRemark.totalCount} Posts</h4>
        {data.allMarkdownRemark.edges.map(({ node }) => (
          <NoteField note={node} key={node.id} />
        ))}
      </div>
    </Layout>
  )
}

export const query = graphql`
  query {
    allMarkdownRemark(sort: { fields: [frontmatter___date], order: DESC }) {
      totalCount
      edges {
        node {
          id
          frontmatter {
            title
            categories
            date
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
