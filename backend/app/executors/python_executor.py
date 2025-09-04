import ast
import sys
import io
import traceback
import time
from typing import List, Dict, Any, Optional
from contextlib import redirect_stdout, redirect_stderr

from ..models import ExecutionStep, StackFrame, Variable, ValidationResult, ValidationError


class ExecutionResult:
    def __init__(self):
        self.steps: List[ExecutionStep] = []
        self.output: List[str] = []
        self.status: str = "completed"
        self.execution_time: float = 0.0
        self.error: Optional[str] = None


class PythonTracer:
    """Traceur pour capturer l'exécution pas-à-pas du code Python."""

    def __init__(self):
        self.steps = []
        self.current_step = 0
        self.output_buffer = []
        self.globals_dict = {}
        self.locals_dict = {}

    def trace_calls(self, frame, event, arg):
        """Fonction de traçage appelée à chaque événement."""
        if event == 'line':
            self.capture_step(frame)
        elif event == 'call':
            self.capture_step(frame, is_call=True)
        elif event == 'return':
            self.capture_step(frame, is_return=True, return_value=arg)
        return self.trace_calls

    def capture_step(self, frame, is_call=False, is_return=False, return_value=None):
        """Capture l'état actuel de l'exécution."""
        try:
            # Extraire les variables locales et globales
            locals_vars = []
            globals_vars = []

            # Variables locales
            for name, value in frame.f_locals.items():
                if not name.startswith('__'):
                    locals_vars.append(Variable(
                        name=name,
                        value=self.format_value(value),
                        type=type(value).__name__,
                        scope="local"
                    ))

            # Variables globales (seulement celles définies par l'utilisateur)
            for name, value in frame.f_globals.items():
                if not name.startswith('__') and name not in ['sys', 'traceback', 'io']:
                    globals_vars.append(Variable(
                        name=name,
                        value=self.format_value(value),
                        type=type(value).__name__,
                        scope="global"
                    ))

            # Créer le frame de pile
            stack_frame = StackFrame(
                function_name=frame.f_code.co_name,
                line=frame.f_lineno,
                locals=locals_vars,
                globals=globals_vars
            )

            # Créer l'étape d'exécution
            step = ExecutionStep(
                line=frame.f_lineno,
                step=self.current_step,
                stack=[stack_frame],
                output=self.output_buffer.copy()
            )

            self.steps.append(step)
            self.current_step += 1

        except Exception as e:
            # En cas d'erreur lors du traçage, on continue silencieusement
            pass

    def format_value(self, value):
        """Formate une valeur pour l'affichage."""
        try:
            if isinstance(value, (int, float, str, bool, type(None))):
                return value
            elif isinstance(value, (list, tuple)):
                return [self.format_value(item) for item in value[:10]]  # Limite à 10 éléments
            elif isinstance(value, dict):
                return {k: self.format_value(v) for k, v in list(value.items())[:10]}
            else:
                return str(value)[:100]  # Limite la longueur des chaînes
        except:
            return "<non-serializable>"


class PythonExecutor:
    """Exécuteur pour le code Python avec traçage."""

    def __init__(self):
        self.tracer = PythonTracer()

    async def execute_with_trace(self, code: str, input_data: Optional[str] = None, timeout: int = 30) -> ExecutionResult:
        """Exécute le code Python avec traçage complet."""
        result = ExecutionResult()
        start_time = time.time()

        try:
            # Préparer l'environnement d'exécution
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()

            # Réinitialiser le traceur
            self.tracer = PythonTracer()

            # Si des données d'entrée sont fournies, préparer sys.stdin
            if input_data:
                sys.stdin = io.StringIO(input_data)

            # Rediriger stdout et stderr
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                # Activer le traçage
                sys.settrace(self.tracer.trace_calls)

                # Exécuter le code
                exec_globals = {"__builtins__": __builtins__}
                exec(code, exec_globals)

                # Désactiver le traçage
                sys.settrace(None)

            # Capturer la sortie
            output = stdout_buffer.getvalue()
            error_output = stderr_buffer.getvalue()

            if output:
                result.output = output.strip().split('\n')
            if error_output:
                result.error = error_output
                result.status = "error"

            # Récupérer les étapes de traçage
            result.steps = self.tracer.steps

        except Exception as e:
            result.error = str(e)
            result.status = "error"
            # Ajouter une étape d'erreur
            if not result.steps:
                error_step = ExecutionStep(
                    line=1,
                    step=0,
                    stack=[],
                    output=[],
                    error=str(e)
                )
                result.steps = [error_step]

        finally:
            # Nettoyer
            sys.settrace(None)
            if hasattr(sys.stdin, 'close'):
                sys.stdin.close()
            sys.stdin = sys.__stdin__

            result.execution_time = time.time() - start_time

        return result

    async def validate_syntax(self, code: str) -> ValidationResult:
        """Valide la syntaxe du code Python."""
        result = ValidationResult(is_valid=True)

        try:
            # Tenter de parser le code
            ast.parse(code)
        except SyntaxError as e:
            result.is_valid = False
            error = ValidationError(
                line=e.lineno or 1,
                column=e.offset or 1,
                message=e.msg or "Erreur de syntaxe",
                type="SyntaxError"
            )
            result.errors = [error]
        except Exception as e:
            result.is_valid = False
            error = ValidationError(
                line=1,
                column=1,
                message=str(e),
                type=type(e).__name__
            )
            result.errors = [error]

        return result
