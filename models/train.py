import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
import joblib
import os

# Configuration
os.makedirs('results', exist_ok=True)
os.makedirs('model_artifacts', exist_ok=True)

def train_and_evaluate(processed_data_path):
    print(f"Chargement des données prétraitées : {processed_data_path}")
    df = pd.read_csv(processed_data_path)
    
    target_col = "Stage de l'IRC"
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # 1. Split Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 2. GridSearch XGBoost avec Mesures Anti-Overfitting
    print("\n--- Optimisation XGBoost (GridSearch) ---")
    xgb = XGBClassifier(
        use_label_encoder=False, 
        eval_metric='mlogloss', 
        random_state=42,
        reg_lambda=2,        # Régularisation L2
        tree_method='hist'
    )
    
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5],
        'learning_rate': [0.05, 0.1],
        'subsample': [0.8],
        'colsample_bytree': [0.8]
    }
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    grid = GridSearchCV(xgb, param_grid, cv=cv, scoring='f1_macro', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    best_xgb = grid.best_estimator_
    print(f"Meilleurs paramètres XGB : {grid.best_params_}")

    # 3. Comparaison avec Random Forest (Optimisé anti-overfitting)
    print("\n--- Évaluation Random Forest ---")
    rf = RandomForestClassifier(
        n_estimators=200, 
        class_weight='balanced', 
        max_samples=0.8,     # Utilise seulement 80% des données par arbre (Subsampling)
        max_features='sqrt',  # Réduit le nombre de variables testées par noeud
        max_depth=10,        # Limite la profondeur pour éviter de "mémoriser" le bruit
        random_state=42
    )
    rf_scores = cross_val_score(rf, X_train, y_train, cv=cv, scoring='f1_macro')
    print(f"RF CV F1-Score (Macro): {rf_scores.mean():.4f} (+/- {rf_scores.std():.4f})")
    rf.fit(X_train, y_train)

    # 4. Évaluation sur Test Set
    y_pred_xgb = best_xgb.predict(X_test)
    y_pred_rf = rf.predict(X_test)
    
    f1_xgb = f1_score(y_test, y_pred_xgb, average='macro')
    f1_rf = f1_score(y_test, y_pred_rf, average='macro')
    
    print(f"\nTest F1-Score Macro -> XGBoost: {f1_xgb:.4f}, Random Forest: {f1_rf:.4f}")
    
    # Choix du modèle final
    best_model = best_xgb if f1_xgb >= f1_rf else rf
    model_name = "XGBoost" if f1_xgb >= f1_rf else "Random Forest"
    
    print(f"\nModèle sélectionné : {model_name}")
    report = classification_report(y_test, best_model.predict(X_test))
    print(report)

    # 5. Overfitting Check
    train_acc = accuracy_score(y_train, best_model.predict(X_train))
    test_acc = accuracy_score(y_test, best_model.predict(X_test))
    print(f"Overfitting Check - Train Acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}")

    # 6. Sauvegardes
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, best_model.predict(X_test))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges')
    plt.title(f"Matrice de Confusion Final ({model_name})")
    plt.savefig('results/final_optimized_cm.png')

    joblib.dump(best_model, f'model_artifacts/best_model_{model_name.lower().replace(" ","_")}.joblib')
    
    with open('results/training_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT D'ENTRAINEMENT MASTER - {pd.Timestamp.now()}\n")
        f.write(f"Modèle Sélectionné : {model_name}\n")
        f.write(f"XGB Test F1: {f1_xgb:.4f}, RF Test F1: {f1_rf:.4f}\n")
        f.write(f"Train Acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}\n\n")
        f.write(report)

if __name__ == "__main__":
    train_and_evaluate('processed/ckd_processed.csv')
