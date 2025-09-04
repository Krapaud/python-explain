'use client'

import * as monaco from 'monaco-editor'
import { useEffect, useRef } from 'react'

interface CodeEditorProps {
  code: string
  language: 'python' | 'javascript' | 'c'
  onChange: (code: string) => void
  currentLine?: number
}

export default function CodeEditor({
  code,
  language,
  onChange,
  currentLine
}: CodeEditorProps) {
  const editorRef = useRef<HTMLDivElement>(null)
  const monacoEditorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null)

  useEffect(() => {
    if (editorRef.current && !monacoEditorRef.current) {
      // Configuration de Monaco Editor
      monaco.editor.defineTheme('pythonGeeksTheme', {
        base: 'vs-dark',
        inherit: true,
        rules: [
          { token: 'comment', foreground: '6a9955' },
          { token: 'keyword', foreground: '569cd6' },
          { token: 'string', foreground: 'ce9178' },
          { token: 'number', foreground: 'b5cea8' },
        ],
        colors: {
          'editor.background': '#1e1e1e',
          'editor.foreground': '#d4d4d4',
          'editor.lineHighlightBackground': '#2d2d30',
          'editorLineNumber.foreground': '#858585',
          'editorCursor.foreground': '#ffffff',
        }
      })

      monacoEditorRef.current = monaco.editor.create(editorRef.current, {
        value: code,
        language: getMonacoLanguage(language),
        theme: 'pythonGeeksTheme',
        fontSize: 14,
        lineNumbers: 'on',
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        automaticLayout: true,
        wordWrap: 'on',
        tabSize: 4,
        insertSpaces: true,
      })

      monacoEditorRef.current.onDidChangeModelContent(() => {
        const value = monacoEditorRef.current?.getValue() || ''
        onChange(value)
      })
    }

    return () => {
      if (monacoEditorRef.current) {
        monacoEditorRef.current.dispose()
        monacoEditorRef.current = null
      }
    }
  }, [])

  useEffect(() => {
    if (monacoEditorRef.current && code !== monacoEditorRef.current.getValue()) {
      monacoEditorRef.current.setValue(code)
    }
  }, [code])

  useEffect(() => {
    if (monacoEditorRef.current) {
      const model = monacoEditorRef.current.getModel()
      if (model) {
        monaco.editor.setModelLanguage(model, getMonacoLanguage(language))
      }
    }
  }, [language])

  useEffect(() => {
    if (monacoEditorRef.current && currentLine) {
      // Surligner la ligne courante
      monacoEditorRef.current.deltaDecorations([], [
        {
          range: new monaco.Range(currentLine, 1, currentLine, 1),
          options: {
            isWholeLine: true,
            className: 'current-line-highlight',
            glyphMarginClassName: 'current-line-glyph'
          }
        }
      ])

      // Centrer la vue sur la ligne courante
      monacoEditorRef.current.revealLineInCenter(currentLine)
    }
  }, [currentLine])

  const getMonacoLanguage = (lang: string): string => {
    switch (lang) {
      case 'python': return 'python'
      case 'javascript': return 'javascript'
      case 'c': return 'c'
      default: return 'python'
    }
  }

  return (
    <div className="h-full w-full">
      <div
        ref={editorRef}
        className="h-full w-full"
        style={{ minHeight: '400px' }}
      />
      <style jsx global>{`
        .current-line-highlight {
          background-color: rgba(255, 255, 0, 0.1) !important;
        }
        .current-line-glyph {
          background-color: #ffff00 !important;
          width: 3px !important;
        }
      `}</style>
    </div>
  )
}
