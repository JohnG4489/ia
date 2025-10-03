"""
Utilitaires pour la manipulation de données
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


def load_dataset(path, file_type='csv', **kwargs):
    """
    Charge un dataset depuis un fichier.
    
    Args:
        path (str): Chemin vers le fichier
        file_type (str): Type de fichier ('csv', 'json', 'parquet')
        **kwargs: Arguments additionnels pour pandas
    
    Returns:
        pd.DataFrame: Dataset chargé
    """
    if file_type == 'csv':
        return pd.read_csv(path, **kwargs)
    elif file_type == 'json':
        return pd.read_json(path, **kwargs)
    elif file_type == 'parquet':
        return pd.read_parquet(path, **kwargs)
    else:
        raise ValueError(f"Type de fichier non supporté: {file_type}")


def preprocess_data(df, target_column=None, scale_features=True, encode_categorical=True):
    """
    Préprocesse les données pour le machine learning.
    
    Args:
        df (pd.DataFrame): Dataset à preprocesser
        target_column (str): Nom de la colonne cible
        scale_features (bool): Normaliser les features numériques
        encode_categorical (bool): Encoder les variables catégorielles
    
    Returns:
        tuple: (X, y, preprocessors)
    """
    df_processed = df.copy()
    preprocessors = {}
    
    # Séparer features et target
    if target_column:
        y = df_processed[target_column]
        X = df_processed.drop(target_column, axis=1)
    else:
        X = df_processed
        y = None
    
    # Encoder les variables catégorielles
    if encode_categorical:
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            preprocessors[f'{col}_encoder'] = le
    
    # Normaliser les features numériques
    if scale_features:
        scaler = StandardScaler()
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        X[numeric_columns] = scaler.fit_transform(X[numeric_columns])
        preprocessors['scaler'] = scaler
    
    return X, y, preprocessors


def split_data(X, y, test_size=0.2, validation_size=0.1, random_state=42):
    """
    Divise les données en train/validation/test.
    
    Args:
        X: Features
        y: Target
        test_size (float): Proportion du test set
        validation_size (float): Proportion du validation set
        random_state (int): Seed pour la reproductibilité
    
    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    # Division train/test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Division train/validation
    val_size_adjusted = validation_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size_adjusted, random_state=random_state
    )
    
    return X_train, X_val, X_test, y_train, y_val, y_test