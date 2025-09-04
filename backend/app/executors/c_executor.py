"""
Exécuteur C utilisant GCC
"""

import asyncio
import tempfile
import os
from typing import Optional
from ..models import ValidationResult, ValidationError
from .python_executor import ExecutionResult


class CExecutor:
    """Exécuteur pour le code C."""

    def __init__(self):
        self.gcc_path = "gcc"

    async def execute_with_trace(self, code: str, input_data: Optional[str] = None, timeout: int = 30) -> ExecutionResult:
        """Exécute le code C avec compilation et exécution."""
        result = ExecutionResult()

        try:
            # Créer des fichiers temporaires
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as source_file:
                source_file.write(code)
                source_path = source_file.name

            # Nom du fichier exécutable
            executable_path = source_path.replace('.c', '')

            # Compiler
            compile_process = await asyncio.create_subprocess_exec(
                self.gcc_path, '-o', executable_path, source_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            compile_stdout, compile_stderr = await compile_process.communicate()

            if compile_process.returncode != 0:
                result.error = f"Erreur de compilation: {compile_stderr.decode()}"
                result.status = "error"
                return result

            # Exécuter
            execute_process = await asyncio.create_subprocess_exec(
                executable_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE if input_data else None
            )

            input_bytes = input_data.encode() if input_data else None
            stdout, stderr = await asyncio.wait_for(
                execute_process.communicate(input=input_bytes),
                timeout=timeout
            )

            if stdout:
                result.output = stdout.decode().strip().split('\n')

            if stderr:
                result.error = stderr.decode()
                result.status = "error"

            # Créer une étape simple
            from ..models import ExecutionStep, StackFrame

            step = ExecutionStep(
                line=1,
                step=0,
                stack=[StackFrame(
                    function_name="main",
                    line=1,
                    locals=[],
                    globals=[]
                )],
                output=result.output
            )
            result.steps = [step]

        except asyncio.TimeoutError:
            result.error = "Timeout d'exécution dépassé"
            result.status = "error"
        except Exception as e:
            result.error = str(e)
            result.status = "error"
        finally:
            # Nettoyer les fichiers temporaires
            for path in [source_path, executable_path]:
                if os.path.exists(path):
                    os.unlink(path)

        return result

    async def validate_syntax(self, code: str) -> ValidationResult:
        """Valide la syntaxe C en tentant une compilation."""
        result = ValidationResult(is_valid=True)

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Tenter la compilation
            process = await asyncio.create_subprocess_exec(
                self.gcc_path, '-fsyntax-only', temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                result.is_valid = False
                error = ValidationError(
                    line=1,
                    column=1,
                    message=stderr.decode().strip(),
                    type="CompileError"
                )
                result.errors = [error]

        except Exception as e:
            result.is_valid = False
            error = ValidationError(
                line=1,
                column=1,
                message=str(e),
                type="Error"
            )
            result.errors = [error]
        finally:
            if 'temp_file' in locals():
                os.unlink(temp_file)

        return result
