# Python Geeks - Code Visualizer & Tutor

Un clone moderne de [Python Tutor](https://pythontutor.com) avec des fonctionnalités avancées pour l'apprentissage de la programmation.

## 🚀 Démarrage rapide

### Prérequis
- Docker et Docker Compose
- Git

### Installation en 3 étapes

1. **Cloner le projet**
```bash
git clone <repository-url>
cd python-geeks
```

2. **Démarrer l'application**
```bash
./start.sh
```

3. **Tester l'installation**
```bash
./test.sh
```

### Accès
- **Application** : http://localhost:3000
- **API** : http://localhost:8000/api/docs

## 🎯 Fonctionnalités

### ✅ Fonctionnalités actuelles
- **Éditeur de code** Monaco avec coloration syntaxique
- **Exécution Python** avec traçage pas-à-pas
- **Visualisation** des variables et pile d'appels
- **API REST** complète avec FastAPI
- **Interface moderne** avec Next.js et Tailwind

### 🚧 En développement
- Support JavaScript et C complet
- Visualisation graphique avancée
- Tuteur IA intégré
- Mode collaboratif

## 🏗️ Architecture

```
Frontend (Next.js)     Backend (FastAPI)      Exécuteurs
    ┌─────────┐           ┌─────────┐         ┌─────────┐
    │ Monaco  │    HTTP   │   API   │ Docker  │ Python  │
    │ Editor  │◄─────────►│  REST   │◄───────►│   JS    │
    │ React   │           │ FastAPI │         │   C     │
    └─────────┘           └─────────┘         └─────────┘
         │                      │                   │
         └──────────────────────┼───────────────────┘
                           PostgreSQL
                             Redis
```

## 📁 Structure du projet

```text
python-geeks/
├── frontend/              # Application Next.js
│   ├── src/app/          # Pages et layouts
│   ├── src/components/   # Composants React
│   └── src/types/        # Types TypeScript
├── backend/              # API Python FastAPI
│   ├── app/
│   │   ├── executors/    # Moteurs d'exécution
│   │   ├── models.py     # Modèles Pydantic
│   │   └── main.py       # Point d'entrée API
├── docker/               # Configuration Docker
├── docs/                 # Documentation
├── start.sh             # Script de démarrage
├── test.sh              # Script de test
└── Makefile             # Commandes utiles
```

## 🛠️ Développement

### Commandes utiles
```bash
# Démarrage
./start.sh                    # Démarrer l'application
./test.sh                     # Tester l'installation

# Docker
make dev                      # Mode développement
make clean                    # Nettoyer
docker-compose -f docker/docker-compose.dev.yml logs -f  # Voir les logs

# Tests manuels
curl http://localhost:8000/api/health     # Test API
curl http://localhost:3000                # Test Frontend
```

### Exemple d'utilisation de l'API
```bash
# Exécuter du code Python
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)\n\nprint(factorial(5))",
    "language": "python"
  }'
```

## 🎓 Inspiré par

Ce projet est inspiré par [Python Tutor](https://pythontutor.com/) créé par Philip Guo.

## 📝 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

---

🌟 **Contribuez au projet** en ouvrant des issues ou en proposant des pull requests !
