#!/bin/bash

# Script de démarrage rapide pour Python Geeks

set -e

echo "🚀 Démarrage de Python Geeks..."

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Créer le fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env
fi

# Construire et démarrer les services
echo "🔨 Construction des images Docker..."
docker-compose -f docker/docker-compose.dev.yml build

echo "🚀 Démarrage des services..."
docker-compose -f docker/docker-compose.dev.yml up -d

echo "⏳ Attente du démarrage des services..."
sleep 10

# Vérifier que les services sont en cours d'exécution
if docker-compose -f docker/docker-compose.dev.yml ps | grep -q "Up"; then
    echo "✅ Services démarrés avec succès!"
    echo ""
    echo "🌐 Accès à l'application:"
    echo "   Frontend: http://localhost:3000"
    echo "   API:      http://localhost:8000"
    echo "   Docs:     http://localhost:8000/api/docs"
    echo ""
    echo "📋 Commandes utiles:"
    echo "   Voir les logs:    docker-compose -f docker/docker-compose.dev.yml logs -f"
    echo "   Arrêter:          docker-compose -f docker/docker-compose.dev.yml down"
    echo "   Redémarrer:       docker-compose -f docker/docker-compose.dev.yml restart"
else
    echo "❌ Erreur lors du démarrage des services"
    echo "Vérifiez les logs: docker-compose -f docker/docker-compose.dev.yml logs"
    exit 1
fi
