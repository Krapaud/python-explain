# Python Geeks - Makefile

.PHONY: help install dev build test clean docker-build docker-up docker-down

help: ## Affiche l'aide
	@echo "Commandes disponibles:"
	@echo "  install     - Installe toutes les dépendances"
	@echo "  dev         - Lance l'environnement de développement"
	@echo "  build       - Build l'application pour la production"
	@echo "  test        - Lance tous les tests"
	@echo "  clean       - Nettoie les fichiers temporaires"
	@echo "  docker-build - Build les images Docker"
	@echo "  docker-up   - Lance les services Docker"
	@echo "  docker-down - Arrête les services Docker"

install: ## Installe les dépendances
	@echo "🔧 Installation des dépendances..."
	cd frontend && npm install
	cd backend && pip install -r requirements.txt
	@echo "✅ Installation terminée!"

dev: ## Lance l'environnement de développement
	@echo "🚀 Lancement en mode développement..."
	docker-compose -f docker/docker-compose.dev.yml up

build: ## Build pour la production
	@echo "🏗️ Build de l'application..."
	cd frontend && npm run build
	cd backend && python -m build
	@echo "✅ Build terminé!"

test: ## Lance les tests
	@echo "🧪 Lancement des tests..."
	cd frontend && npm test
	cd backend && pytest
	@echo "✅ Tests terminés!"

clean: ## Nettoie les fichiers temporaires
	@echo "🧹 Nettoyage..."
	cd frontend && rm -rf node_modules dist .next
	cd backend && rm -rf __pycache__ .pytest_cache dist build
	docker system prune -f
	@echo "✅ Nettoyage terminé!"

docker-build: ## Build les images Docker
	@echo "🐳 Build des images Docker..."
	docker-compose -f docker/docker-compose.yml build

docker-up: ## Lance les services Docker
	@echo "🐳 Lancement des services Docker..."
	docker-compose -f docker/docker-compose.yml up -d

docker-down: ## Arrête les services Docker
	@echo "🐳 Arrêt des services Docker..."
	docker-compose -f docker/docker-compose.yml down
