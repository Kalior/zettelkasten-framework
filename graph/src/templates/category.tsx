import { graphql } from "gatsby"

import { PostNode } from "../types"
import { Layout } from "../components/layout"
import { NoteField } from "../components/noteField"

export default ({ data, pageContext }) => {
  const allNotes: PostNode[] = data.allMarkdownRemark.edges.map(
    ({ node }) => node
  )

  return (
    <Layout>
      <div>
        <h4>{`Category: ${pageContext.category}`}</h4>
        <h4>{data.allMarkdownRemark.totalCount} Posts</h4>
        {allNotes.map(node => (
          <NoteField note={node} key={node.id} />
        ))}
      </div>
    </Layout>
  )
}

export const query = graphql`
  query($category: [String!]) {
    allMarkdownRemark(
      filter: { frontmatter: { categories: { in: $category } } }
    ) {
      totalCount
      edges {
        node {
          id
          html
          frontmatter {
            title
            links
            uid
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
