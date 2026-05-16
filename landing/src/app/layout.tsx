import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "DClaw Patent — AI-Powered Patent Management",
  description:
    "AI-powered patent management and IP portfolio automation. Draft claims, search prior art, track deadlines, and manage your patent portfolio with AI.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
