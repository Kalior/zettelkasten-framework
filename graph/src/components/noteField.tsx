import { Shadow } from "./neumorphism"
import { Link } from "gatsby"
import styled from "@emotion/styled"
import { CategoryList } from "./categoryList"

export const NoteField = ({ note }) => {
  return (
    <Shadow style={{ padding: "1em 2em", margin: "2em 1em" }}>
      <CategoryList categories={note.frontmatter.categories} />
      <StyledLink to={note.fields.slug}>
        <Title>
          {note.frontmatter.title} <Date>— {note.frontmatter.date}</Date>
        </Title>

        <p>{note.excerpt}</p>
      </StyledLink>
    </Shadow>
  )
}

const Date = styled.span`
  color: #bbb;
`

const Title = styled.h3`
  margin-bottom: 1em;
`
const StyledLink = styled(Link)`
  text-decoration: none;
  color: inherit;

  :hover {
    text-decoration: underline;
  }
`
