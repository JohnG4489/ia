"""
Utilitaires communs pour les projets d'Intelligence Artificielle
"""

__version__ = "1.0.0"
__author__ = "JohnG4489"

# Imports principaux
from .data_utils import load_dataset, preprocess_data, split_data
from .visualization import plot_confusion_matrix, plot_learning_curve
from .metrics import custom_accuracy, model_evaluation

__all__ = [
    "load_dataset",
    "preprocess_data", 
    "split_data",
    "plot_confusion_matrix",
    "plot_learning_curve",
    "custom_accuracy",
    "model_evaluation"
]