import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "DClaw Patent",
  description: "AI-powered patent management and IP analytics",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
