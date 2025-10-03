# AI Photo & Video Remastering

Une application de remasterisation de photos et vidéos utilisant l'intelligence artificielle.

## Fonctionnalités

- **Enhancement d'images** : Amélioration de la qualité, upscaling, débruitage et correction des couleurs
- **Enhancement de vidéos** : Traitement frame par frame avec stabilisation optionnelle
- **Modèles IA** : Support pour Real-ESRGAN et autres modèles de super-résolution
- **Interface web** : Interface utilisateur simple pour traiter des fichiers individuels
- **Interface CLI** : Outil en ligne de commande pour le traitement par lots
- **Formats supportés** :
  - Images : JPG, PNG, BMP, TIFF, WebP
  - Vidéos : MP4, AVI, MOV, MKV, WMV

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/JohnG4489/ia.git
cd ia
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. (Optionnel) Installer le package :
```bash
pip install -e .
```

## Utilisation

### Interface en ligne de commande

#### Améliorer une image :
```bash
python main.py enhance-image input/photo.jpg --output output/photo_enhanced.jpg --model esrgan --scale 2
```

#### Améliorer une vidéo :
```bash
python main.py enhance-video input/video.mp4 --output output/video_enhanced.mp4 --model esrgan
```

#### Traitement par lots :
```bash
python main.py batch-enhance input_folder/ --output output_folder/ --model esrgan --scale 2
```

### Interface web

Lancer l'interface web :
```bash
python main.py web
```

Puis ouvrir http://localhost:5000 dans votre navigateur.

## Modèles disponibles

- **esrgan** : Real-ESRGAN 4x upscaling model (recommandé)
- **esrgan_anime** : Real-ESRGAN optimisé pour l'anime et l'artwork

## Configuration

La configuration peut être modifiée dans `config.py` :

- Formats de fichiers supportés
- Taille maximale des images
- Paramètres des modèles IA
- Configuration de l'interface web

## Exemples

### Structure des dossiers
```
ia/
├── input/          # Dossier pour les fichiers d'entrée
├── output/         # Dossier pour les fichiers traités
├── uploads/        # Dossier pour les uploads web
├── models/         # Dossier pour les modèles IA
├── src/           # Code source
├── main.py        # Point d'entrée principal
└── requirements.txt
```

### Exemples d'amélioration

L'IA peut améliorer :
- La résolution (upscaling 2x, 4x)
- La netteté et les détails
- La réduction du bruit
- L'équilibre des couleurs
- Le contraste et la luminosité

## Développement

Pour contribuer au projet :

1. Fork le repository
2. Créer une branche pour votre feature
3. Commiter vos changements
4. Pousser vers votre fork
5. Créer une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Dépendances principales

- OpenCV pour le traitement d'images/vidéos
- Real-ESRGAN pour l'upscaling IA
- Flask pour l'interface web
- Click pour l'interface CLI
- PyTorch pour les modèles de deep learning
