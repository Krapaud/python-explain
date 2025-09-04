from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
import json
import logging
from datetime import datetime

from .executors import PythonExecutor, JavaScriptExecutor, CExecutor
from .models import ExecutionRequest, ExecutionResponse, ExecutionStep
from .visualizer import CodeVisualizer

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Python Geeks API",
    description="API pour la visualisation et l'exécution de code",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des exécuteurs
executors = {
    "python": PythonExecutor(),
    "javascript": JavaScriptExecutor(),
    "c": CExecutor(),
}

visualizer = CodeVisualizer()

@app.get("/")
async def root():
    """Point d'entrée principal de l'API."""
    return {
        "message": "Bienvenue sur Python Geeks API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "status": "active"
    }

@app.get("/api/health")
async def health_check():
    """Vérification de l'état de l'API."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "executors": list(executors.keys())
    }

@app.post("/api/execute", response_model=ExecutionResponse)
async def execute_code(request: ExecutionRequest):
    """
    Exécute le code fourni et retourne les étapes d'exécution pour la visualisation.
    """
    try:
        logger.info(f"Exécution demandée pour le langage: {request.language}")

        # Validation du langage
        if request.language not in executors:
            raise HTTPException(
                status_code=400,
                detail=f"Langage non supporté: {request.language}"
            )

        # Obtention de l'exécuteur approprié
        executor = executors[request.language]

        # Exécution du code avec traçage
        execution_result = await executor.execute_with_trace(
            code=request.code,
            input_data=request.input_data,
            timeout=request.timeout
        )

        # Génération de la visualisation
        visualization_data = await visualizer.generate_visualization(
            execution_result, request.language
        )

        # Construction de la réponse
        response = ExecutionResponse(
            steps=execution_result.steps,
            current_step=0,
            total_steps=len(execution_result.steps),
            language=request.language,
            code=request.code,
            status=execution_result.status,
            final_output=execution_result.output,
            execution_time=execution_result.execution_time,
            visualization=visualization_data
        )

        logger.info(f"Exécution terminée avec {len(execution_result.steps)} étapes")
        return response

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'exécution: {str(e)}"
        )

@app.post("/api/validate")
async def validate_code(request: ExecutionRequest):
    """
    Valide la syntaxe du code sans l'exécuter.
    """
    try:
        if request.language not in executors:
            raise HTTPException(
                status_code=400,
                detail=f"Langage non supporté: {request.language}"
            )

        executor = executors[request.language]
        validation_result = await executor.validate_syntax(request.code)

        return {
            "valid": validation_result.is_valid,
            "errors": validation_result.errors,
            "warnings": validation_result.warnings
        }

    except Exception as e:
        logger.error(f"Erreur lors de la validation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la validation: {str(e)}"
        )

@app.get("/api/examples/{language}")
async def get_examples(language: str):
    """
    Récupère des exemples de code pour un langage donné.
    """
    examples_map = {
        "python": [
            {
                "title": "Factorielle récursive",
                "code": """def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

result = factorial(5)
print(f"5! = {result}")""",
                "description": "Calcul de la factorielle en utilisant la récursion"
            },
            {
                "title": "Tri à bulles",
                "code": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers.copy())
print(f"Tableau trié: {sorted_numbers}")""",
                "description": "Algorithme de tri à bulles"
            }
        ],
        "javascript": [
            {
                "title": "Fibonacci récursif",
                "code": """function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

let result = fibonacci(7);
console.log(`Fibonacci(7) = ${result}`);""",
                "description": "Calcul de Fibonacci en récursif"
            }
        ],
        "c": [
            {
                "title": "Hello World",
                "code": """#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}""",
                "description": "Programme Hello World en C"
            }
        ]
    }

    if language not in examples_map:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun exemple disponible pour: {language}"
        )

    return {"examples": examples_map[language]}

@app.get("/api/languages")
async def get_supported_languages():
    """
    Retourne la liste des langages supportés.
    """
    return {
        "languages": [
            {
                "id": "python",
                "name": "Python",
                "version": "3.11",
                "description": "Langage de programmation polyvalent"
            },
            {
                "id": "javascript",
                "name": "JavaScript",
                "version": "ES2023",
                "description": "Langage de programmation pour le web"
            },
            {
                "id": "c",
                "name": "C",
                "version": "C11",
                "description": "Langage de programmation système"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
