# Utils

Ce dossier contient les utilitaires et outils communs utilisés dans les projets.

## Contenu

- **Data Utils** : Fonctions de manipulation de données
- **Model Utils** : Utilitaires pour les modèles
- **Visualization** : Fonctions de visualisation
- **Metrics** : Calcul de métriques personnalisées
- **Config** : Gestion de configuration
- **Logging** : Système de logs
- **Deployment** : Outils de déploiement

## Structure

```
utils/
├── data_utils.py
├── model_utils.py
├── visualization.py
├── metrics.py
├── config.py
├── logging_utils.py
├── deployment.py
└── __init__.py
```

## Usage

```python
from utils import data_utils, visualization
from utils.metrics import custom_accuracy
```

## Standards

- Code documenté avec docstrings
- Tests unitaires inclus
- Compatible Python 3.8+