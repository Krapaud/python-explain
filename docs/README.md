# Python Geeks - Clone de Python Tutor

## 📋 Guide de démarrage rapide

### Prérequis
- Docker et Docker Compose
- Node.js 18+ (pour le développement local)
- Python 3.11+ (pour le développement local)

### Installation

1. **Cloner le projet**
```bash
git clone <repository-url>
cd python-geeks
```

2. **Configuration de l'environnement**
```bash
cp .env.example .env
# Éditer .env selon vos besoins
```

3. **Lancement avec Docker (recommandé)**
```bash
make dev
# ou
docker-compose -f docker/docker-compose.dev.yml up
```

4. **Lancement en mode développement local**
```bash
make install
make dev-local
```

### Accès à l'application
- **Frontend** : http://localhost:3000
- **API Backend** : http://localhost:8000
- **Documentation API** : http://localhost:8000/api/docs

## 🏗️ Architecture

### Frontend (Next.js + TypeScript)
- **Framework** : Next.js 14 avec App Router
- **UI** : Tailwind CSS + Composants personnalisés
- **Éditeur** : Monaco Editor
- **Visualisation** : D3.js + Canvas
- **State Management** : Zustand

### Backend (Python FastAPI)
- **Framework** : FastAPI
- **Base de données** : PostgreSQL
- **Cache** : Redis
- **Exécution** : Conteneurs Docker sécurisés
- **Traçage** : Système de traçage personnalisé

### Exécuteurs de code
- **Python** : Traçage avec `sys.settrace()`
- **JavaScript** : Node.js avec V8 Inspector
- **C/C++** : GDB pour le débogage

## 🔧 Développement

### Structure du projet
```
python-geeks/
├── frontend/          # Application React/Next.js
│   ├── src/
│   │   ├── app/       # Pages et layouts
│   │   ├── components/ # Composants réutilisables
│   │   └── types/     # Types TypeScript
├── backend/           # API Python FastAPI
│   ├── app/
│   │   ├── executors/ # Moteurs d'exécution
│   │   ├── models.py  # Modèles Pydantic
│   │   └── main.py    # Point d'entrée
├── visualizer/        # Moteur de visualisation
├── executor/          # Conteneurs d'exécution
└── docker/           # Configuration Docker
```

### Commandes utiles

```bash
# Installation des dépendances
make install

# Développement
make dev              # Avec Docker
make dev-local       # Local

# Tests
make test            # Tous les tests
make test-frontend   # Tests frontend
make test-backend    # Tests backend

# Build
make build           # Build production

# Nettoyage
make clean           # Nettoie les fichiers temporaires
```

### API Endpoints

- `POST /api/execute` - Exécuter du code
- `POST /api/validate` - Valider la syntaxe
- `GET /api/examples/{language}` - Exemples de code
- `GET /api/languages` - Langages supportés
- `GET /api/health` - État de l'API

## 🎯 Fonctionnalités

### ✅ Implémentées
- [x] Éditeur de code Monaco
- [x] Exécution Python avec traçage
- [x] Interface de visualisation basique
- [x] API REST FastAPI
- [x] Configuration Docker

### 🚧 En cours
- [ ] Visualisation avancée des données
- [ ] Support JavaScript complet
- [ ] Support C/C++
- [ ] Tuteur IA intégré
- [ ] Sauvegarde des sessions
- [ ] Partage de code

### 📋 À venir
- [ ] Mode collaboratif
- [ ] Plugins pour IDE
- [ ] Support de plus de langages
- [ ] Analyses de performance
- [ ] Interface mobile

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🎓 Inspiré par

Ce projet est inspiré par [Python Tutor](https://pythontutor.com/) créé par Philip Guo, un outil formidable pour l'apprentissage de la programmation.
