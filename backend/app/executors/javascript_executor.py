"""
Exécuteur JavaScript utilisant Node.js
"""

import asyncio
import json
import tempfile
import os
from typing import Optional
from ..models import ValidationResult, ValidationError
from .python_executor import ExecutionResult


class JavaScriptExecutor:
    """Exécuteur pour le code JavaScript."""

    def __init__(self):
        self.node_path = "node"  # Chemin vers Node.js

    async def execute_with_trace(self, code: str, input_data: Optional[str] = None, timeout: int = 30) -> ExecutionResult:
        """Exécute le code JavaScript avec traçage."""
        result = ExecutionResult()

        try:
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Exécuter avec Node.js
            process = await asyncio.create_subprocess_exec(
                self.node_path, temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )

            if stdout:
                result.output = stdout.decode().strip().split('\n')

            if stderr:
                result.error = stderr.decode()
                result.status = "error"

            # Pour le moment, créer une étape simple
            from ..models import ExecutionStep, StackFrame, Variable

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
            # Nettoyer le fichier temporaire
            if 'temp_file' in locals():
                os.unlink(temp_file)

        return result

    async def validate_syntax(self, code: str) -> ValidationResult:
        """Valide la syntaxe JavaScript."""
        result = ValidationResult(is_valid=True)

        try:
            # Utiliser Node.js pour vérifier la syntaxe
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                # Code de validation
                validation_code = f"""
try {{
    new Function({json.dumps(code)});
    console.log('SYNTAX_OK');
}} catch (e) {{
    console.log('SYNTAX_ERROR:' + e.message);
}}
"""
                f.write(validation_code)
                temp_file = f.name

            process = await asyncio.create_subprocess_exec(
                self.node_path, temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            output = stdout.decode().strip()

            if not output.startswith('SYNTAX_OK'):
                result.is_valid = False
                error_msg = output.replace('SYNTAX_ERROR:', '') if 'SYNTAX_ERROR:' in output else "Erreur de syntaxe"
                error = ValidationError(
                    line=1,
                    column=1,
                    message=error_msg,
                    type="SyntaxError"
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
