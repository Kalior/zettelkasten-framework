import React from "react"

import Header from "./header"

export const Layout = ({ children }) => (
  <div style={{ minHeight: "100vh", backgroundColor: "#EFEEEE" }}>
    <Header />
    <div
      style={{
        padding: `3rem`,
        color: "#2e414f",
      }}
    >
      {children}
    </div>
  </div>
)
