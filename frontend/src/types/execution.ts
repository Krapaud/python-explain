export interface Variable {
  name: string
  value: any
  type: string
  scope: string
}

export interface StackFrame {
  function_name: string
  line: number
  locals: Variable[]
  globals: Variable[]
}

export interface ExecutionStep {
  line: number
  step: number
  stack: StackFrame[]
  heap: Record<string, any>
  output: string[]
  error?: string
}

export interface ExecutionState {
  steps: ExecutionStep[]
  current_step: number
  total_steps: number
  language: 'python' | 'javascript' | 'c'
  code: string
  status: 'running' | 'completed' | 'error'
  final_output: string[]
  execution_time: number
}

export interface CodePosition {
  line: number
  column: number
}

export interface VisualizationNode {
  id: string
  type: 'variable' | 'function' | 'object' | 'array'
  name: string
  value: any
  position: { x: number; y: number }
  connections: string[]
}
