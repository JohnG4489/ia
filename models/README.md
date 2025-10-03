# Models

Ce dossier contient les modèles pré-entraînés et sauvegardés.

## Contenu

- **Pre-trained Models** : Modèles téléchargés (BERT, GPT, etc.)
- **Trained Models** : Modèles entraînés sur nos données
- **Checkpoints** : Points de sauvegarde pendant l'entraînement
- **Model Configs** : Configurations et hyperparamètres
- **Weights** : Poids des modèles sauvegardés

## Structure

```
models/
├── pre-trained/
├── trained/
├── checkpoints/
├── configs/
└── weights/
```

## Formats

- TensorFlow SavedModel (.pb)
- PyTorch (.pth, .pt)
- ONNX (.onnx)
- Pickle (.pkl)
- HDF5 (.h5)

## Organisation

- Un dossier par projet
- Versioning des modèles
- Documentation des performances
- Métadonnées d'entraînement