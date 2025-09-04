'use client'

import { Pause, Play, RotateCcw, Settings } from 'lucide-react'

interface ToolbarProps {
  language: 'python' | 'javascript' | 'c'
  onLanguageChange: (language: 'python' | 'javascript' | 'c') => void
  onExecute: () => void
  isExecuting: boolean
}

export default function Toolbar({
  language,
  onLanguageChange,
  onExecute,
  isExecuting
}: ToolbarProps) {
  return (
    <div className="bg-white border-b border-gray-300 p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-bold text-gray-800">
            Python Geeks
          </h1>

          <select
            value={language}
            onChange={(e) => onLanguageChange(e.target.value as any)}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="c">C</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={onExecute}
            disabled={isExecuting}
            className="btn-primary flex items-center space-x-2"
          >
            {isExecuting ? (
              <>
                <Pause className="w-4 h-4" />
                <span>Exécution...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Exécuter</span>
              </>
            )}
          </button>

          <button className="btn-secondary">
            <RotateCcw className="w-4 h-4" />
          </button>

          <button className="btn-secondary">
            <Settings className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}
