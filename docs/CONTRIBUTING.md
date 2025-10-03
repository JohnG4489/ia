# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet d'Intelligence Artificielle !

## 🚀 Comment Contribuer

### 1. Fork et Clone

1. Fork ce repository
2. Clonez votre fork localement :
   ```bash
   git clone https://github.com/VOTRE_USERNAME/ia.git
   cd ia
   ```

### 2. Configuration de l'Environnement

1. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### 3. Développement

1. Créez une nouvelle branche :
   ```bash
   git checkout -b feature/nom-de-votre-feature
   ```

2. Effectuez vos modifications
3. Ajoutez des tests si nécessaire
4. Documentez votre code

### 4. Standards de Code

- **Python** : Suivez PEP 8
- **Formatage** : Utilisez `black` pour le formatage
- **Linting** : Utilisez `flake8`
- **Tests** : Ajoutez des tests avec `pytest`
- **Documentation** : Documentez avec des docstrings

```bash
# Formatage
black .

# Linting  
flake8 .

# Tests
pytest
```

### 5. Structure des Commits

Utilisez des messages de commit clairs :
```
type(scope): description

feat(nlp): ajouter modèle de sentiment analysis
fix(data): corriger preprocessing des images
docs(readme): mettre à jour documentation
```

### 6. Pull Request

1. Poussez votre branche :
   ```bash
   git push origin feature/nom-de-votre-feature
   ```

2. Créez une Pull Request avec :
   - Description claire des changements
   - Référence aux issues liées
   - Screenshots si applicable
   - Tests qui passent

## 📁 Organisation des Contributions

### Nouveaux Projets

Créez un nouveau dossier dans la catégorie appropriée :
```
category/
└── nom-du-projet/
    ├── README.md
    ├── src/
    ├── tests/
    ├── data/
    ├── notebooks/
    └── requirements.txt
```

### Documentation

- Chaque projet doit avoir un README.md
- Utilisez Jupyter notebooks pour les tutoriels
- Documentez les APIs et fonctions

### Datasets

- Ajoutez des métadonnées pour chaque dataset
- Respectez les licences
- Documentez les sources
- Utilisez Git LFS pour les gros fichiers

## 🔍 Review Process

1. **Automated checks** : Tests, linting, formatting
2. **Code review** : Review par les maintainers
3. **Testing** : Validation sur différents environnements
4. **Documentation** : Vérification de la documentation

## 🎯 Types de Contributions

- **Code** : Nouveaux algorithmes, optimisations
- **Documentation** : Guides, tutoriels, exemples
- **Datasets** : Nouveaux jeux de données
- **Research** : Reproductions d'articles, benchmarks
- **Bug fixes** : Corrections de bugs
- **Tests** : Amélioration de la couverture de tests

## 📋 Checklist PR

- [ ] Code formaté avec `black`
- [ ] Linting passé avec `flake8`
- [ ] Tests ajoutés/mis à jour
- [ ] Tests passent
- [ ] Documentation mise à jour
- [ ] README du projet ajouté/mis à jour
- [ ] Changements testés localement

## 🤝 Code de Conduite

- Soyez respectueux et inclusif
- Acceptez les critiques constructives
- Concentrez-vous sur ce qui est le mieux pour la communauté
- Montrez de l'empathie envers les autres membres

## 💬 Questions ?

- Ouvrez une issue pour les questions générales
- Utilisez les discussions GitHub pour les échanges
- Contactez les maintainers pour les questions spécifiques

Merci de contribuer à l'avancement de l'Intelligence Artificielle ! 🚀