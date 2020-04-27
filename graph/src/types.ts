export interface PostFrontMatter {
  title: string
  links: string[]
  uid: string
  categories: string[]
}

export interface PostFields {
  slug: string
}

export interface PostNode {
  id: string
  html: string
  frontmatter: PostFrontMatter
  excerpt: string
  fields: PostFields
}
