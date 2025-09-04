from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class LanguageType(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    C = "c"

class ExecutionStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"

class Variable(BaseModel):
    name: str
    value: Any
    type: str
    scope: str

class StackFrame(BaseModel):
    function_name: str
    line: int
    locals: List[Variable] = []
    globals: List[Variable] = []

class ExecutionStep(BaseModel):
    line: int
    step: int
    stack: List[StackFrame]
    heap: Dict[str, Any] = {}
    output: List[str] = []
    error: Optional[str] = None

class ExecutionRequest(BaseModel):
    code: str = Field(..., description="Code à exécuter")
    language: LanguageType = Field(..., description="Langage de programmation")
    input_data: Optional[str] = Field(None, description="Données d'entrée pour le programme")
    timeout: int = Field(30, description="Timeout en secondes", ge=1, le=60)

class ExecutionResponse(BaseModel):
    steps: List[ExecutionStep]
    current_step: int = 0
    total_steps: int
    language: LanguageType
    code: str
    status: ExecutionStatus
    final_output: List[str] = []
    execution_time: float
    visualization: Optional[Dict[str, Any]] = None

class ValidationError(BaseModel):
    line: int
    column: int
    message: str
    type: str

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []

class VisualizationNode(BaseModel):
    id: str
    type: str
    name: str
    value: Any
    position: Dict[str, float]
    connections: List[str] = []

class VisualizationData(BaseModel):
    nodes: List[VisualizationNode] = []
    edges: List[Dict[str, Any]] = []
    layout: str = "hierarchical"
