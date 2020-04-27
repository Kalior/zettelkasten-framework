import { Graph } from "react-d3-graph"

import { PostNode } from "../types"

interface GraphNode {
  id: string
}
interface GraphLink {
  source: string
  target: string
}
interface GraphData {
  nodes: GraphNode[]
  links: GraphLink[]
}

interface GraphContainerProps {
  allNotes: PostNode[]
  onClickNode: CallableFunction
  highlightNode?: PostNode
  width?: number
  height?: number
}

export const GraphContainer: React.FC<GraphContainerProps> = ({
  allNotes,
  onClickNode,
  highlightNode = { frontmatter: { uid: "" } },
  width = 860,
  height = 550,
}) => {
  const nodes: GraphNode[] = allNotes.map(node => ({
    id: node.frontmatter.uid,
    title: node.frontmatter.title,
    color:
      node.frontmatter.uid == highlightNode.frontmatter.uid
        ? "#fb9a99"
        : "#2e414f",
  }))

  const externalLinks = [].concat(
    ...allNotes.map(node =>
      node.frontmatter.links
        .filter(link => !allNotes.some(node => link == node.frontmatter.uid))
        .map(link => ({
          id: link,
          title: " ",
          symbolType: link.slice(0, 4) == "http" ? "square" : "circle",
          color: link.slice(0, 4) == "http" ? "#b2df8a" : "#a6cee3",
        }))
    )
  )

  const allNodes = [].concat(nodes, externalLinks)

  const links: GraphLink[] = [].concat(
    ...allNotes.map(node =>
      node.frontmatter.links.map(link => ({
        source: node.frontmatter.uid,
        target: link,
      }))
    )
  )

  const graphData: GraphData = {
    nodes: allNodes,
    links: links,
  }

  const config = {
    nodeHighlightBehavior: true,
    highlightOpacity: 0.3,
    node: {
      labelProperty: "title",
      color: "#2e414f",
    },
    link: {
      type: "STRAIGHT",
    },
    directed: false,
    width: width,
    height: height,
  }

  return (
    <Graph
      id="graph-id"
      data={graphData}
      config={config}
      onClickNode={onClickNode}
    />
  )
}
