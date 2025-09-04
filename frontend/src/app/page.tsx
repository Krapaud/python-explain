'use client'

import CodeEditor from '@/components/CodeEditor'
import Toolbar from '@/components/Toolbar'
import Visualizer from '@/components/Visualizer'
import { ExecutionState } from '@/types/execution'
import { useState } from 'react'

export default function Home() {
  const [code, setCode] = useState(`def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

result = factorial(5)
print(f"5! = {result}")`)

  const [language, setLanguage] = useState<'python' | 'javascript' | 'c'>('python')
  const [executionState, setExecutionState] = useState<ExecutionState | null>(null)
  const [isExecuting, setIsExecuting] = useState(false)

  const handleExecute = async () => {
    setIsExecuting(true)
    try {
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          language,
        }),
      })

      const result = await response.json()
      setExecutionState(result)
    } catch (error) {
      console.error('Erreur lors de l\'exécution:', error)
    } finally {
      setIsExecuting(false)
    }
  }

  return (
    <main className="flex h-screen bg-gray-100">
      {/* Sidebar gauche - Éditeur de code */}
      <div className="w-1/2 flex flex-col border-r border-gray-300">
        <Toolbar
          language={language}
          onLanguageChange={setLanguage}
          onExecute={handleExecute}
          isExecuting={isExecuting}
        />
        <div className="flex-1">
          <CodeEditor
            code={code}
            language={language}
            onChange={setCode}
          />
        </div>
      </div>

      {/* Sidebar droite - Visualiseur */}
      <div className="w-1/2 flex flex-col">
        <div className="bg-white border-b border-gray-300 p-4">
          <h2 className="text-lg font-semibold text-gray-800">
            Visualisation du code
          </h2>
        </div>
        <div className="flex-1">
          <Visualizer
            executionState={executionState}
            isExecuting={isExecuting}
          />
        </div>
      </div>
    </main>
  )
}
