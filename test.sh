#!/bin/bash

# Script de test pour vérifier que tout fonctionne

echo "🧪 Test de l'installation de Python Geeks..."

# Test 1: Vérifier que les services sont en cours d'exécution
echo "1. Vérification des services Docker..."
if docker-compose -f docker/docker-compose.dev.yml ps | grep -q "Up"; then
    echo "✅ Services Docker actifs"
else
    echo "❌ Services Docker non actifs"
    echo "Démarrez-les avec: ./start.sh"
    exit 1
fi

# Test 2: Test de l'API backend
echo "2. Test de l'API backend..."
if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
    echo "✅ API backend accessible"
else
    echo "❌ API backend non accessible"
    echo "Vérifiez les logs: docker-compose -f docker/docker-compose.dev.yml logs backend"
fi

# Test 3: Test du frontend
echo "3. Test du frontend..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo "✅ Frontend accessible"
else
    echo "❌ Frontend non accessible"
    echo "Vérifiez les logs: docker-compose -f docker/docker-compose.dev.yml logs frontend"
fi

# Test 4: Test d'exécution de code simple
echo "4. Test d'exécution de code Python..."
response=$(curl -s -X POST http://localhost:8000/api/execute \
    -H "Content-Type: application/json" \
    -d '{"code":"print(\"Hello, World!\")", "language":"python"}')

if echo "$response" | grep -q "Hello, World!"; then
    echo "✅ Exécution de code Python fonctionnelle"
else
    echo "❌ Problème avec l'exécution de code"
    echo "Réponse: $response"
fi

echo ""
echo "🎉 Tests terminés!"
echo "🌐 Ouvrez http://localhost:3000 dans votre navigateur pour commencer!"
