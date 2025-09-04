import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Python Geeks - Code Visualizer & Tutor',
  description: 'Un outil moderne de visualisation de code et d\'apprentissage de la programmation',
  keywords: ['python', 'javascript', 'c', 'programming', 'visualization', 'tutor', 'debugger'],
  authors: [{ name: 'Python Geeks Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <div id="root">
          {children}
        </div>
      </body>
    </html>
  )
}
