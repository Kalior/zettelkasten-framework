import React from "react"
import styled from "@emotion/styled"
import { Link } from "gatsby"

interface CategoryListProps {
  categories: string[]
}

export const CategoryList: React.FC<CategoryListProps> = ({ categories }) => (
  <CategoryListContainer>
    {categories.map(category => (
      <CategoryItem key={category}>
        <StyledLink to={`/category/${category}`}>{category}</StyledLink>
      </CategoryItem>
    ))}
  </CategoryListContainer>
)

const StyledLink = styled(Link)`
  text-decoration: none;
  color: inherit;

  :hover {
    text-decoration: underline;
  }
`

const CategoryListContainer = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
  color: #999;
`

const CategoryItem = styled.li`
  display: inline-block;
  ::after {
    content: "•";
    margin: 0px 5px;
  }

  :last-child {
    ::after {
      content: "";
    }
  }
`
