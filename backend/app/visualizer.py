"""
Module de visualisation pour générer des représentations graphiques du code.
"""

from typing import Dict, Any, List
from ..models import VisualizationData, VisualizationNode


class CodeVisualizer:
    """Générateur de visualisations pour le code exécuté."""

    def __init__(self):
        self.node_counter = 0

    async def generate_visualization(self, execution_result, language: str) -> Dict[str, Any]:
        """
        Génère les données de visualisation à partir du résultat d'exécution.
        """
        visualization = VisualizationData()

        if not execution_result.steps:
            return visualization.dict()

        # Prendre la dernière étape pour la visualisation
        last_step = execution_result.steps[-1]

        # Générer des nœuds pour les variables
        for frame in last_step.stack:
            # Variables locales
            for var in frame.locals:
                node = self._create_variable_node(var, "local")
                visualization.nodes.append(node)

            # Variables globales
            for var in frame.globals:
                node = self._create_variable_node(var, "global")
                visualization.nodes.append(node)

        return visualization.dict()

    def _create_variable_node(self, variable, scope_type: str) -> VisualizationNode:
        """Crée un nœud de visualisation pour une variable."""
        self.node_counter += 1

        return VisualizationNode(
            id=f"var_{self.node_counter}",
            type="variable",
            name=variable.name,
            value=variable.value,
            position={
                "x": self.node_counter * 100,
                "y": 50 if scope_type == "local" else 150
            },
            connections=[]
        )
