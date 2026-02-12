import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer
from sklearn.preprocessing import RobustScaler, LabelEncoder
import joblib
import os

# Configuration
os.makedirs('processed', exist_ok=True)
os.makedirs('artifacts', exist_ok=True)

def preprocess_data(file_path):
    print(f"Chargement du dataset : {file_path}")
    df = pd.read_csv(file_path)
    
    # --- 1. Nettoyage Initial ---
    target_col = "Stage de l'IRC"
    if target_col in df.columns:
        df = df[df[target_col] != "0%"]
    
    # Bruit sémantique
    df['Situation Matrimoniale'] = df['Situation Matrimoniale'].astype(str).replace({'Veuf': 'Veuf(ve)', '38%': np.nan})
    df['Etat Général (EG) à l\'Admission'] = df['Etat Général (EG) à l\'Admission'].astype(str).replace({'Aceptable': 'Acceptable', '4%': np.nan})
    df['Conscience'] = df['Conscience'].astype(str).replace({'38%': np.nan})

    # Conversion numérique robuste
    for col in df.columns:
        if col == target_col or col == "ID": continue
        temp = df[col].astype(str).str.replace(',', '.').str.extract(r'([-+]?\d*\.?\d+)')[0]
        converted = pd.to_numeric(temp, errors='coerce')
        if converted.notnull().sum() > 0.15 * len(df):
            df[col] = converted

    # --- 2. Feature Engineering Clinique ---
    print("\n--- Feature Engineering Clinique ---")
    if 'Créatinine (mg/L)' in df.columns:
        df['Creat_mg_dL'] = df['Créatinine (mg/L)'] / 10.0
        
    if 'Urée (g/L)' in df.columns:
        df['Urea_mg_dL'] = df['Urée (g/L)'] * 100.0

    # Ratio Urée / Créatinine
    if 'Urea_mg_dL' in df.columns and 'Creat_mg_dL' in df.columns:
        df['Ratio_Urea_Creat'] = df['Urea_mg_dL'] / (df['Creat_mg_dL'].replace(0, np.nan))
        df['Ratio_Urea_Creat'] = df['Ratio_Urea_Creat'].replace([np.inf, -np.inf], np.nan)
        
    # eGFR (MDRD)
    if 'Creat_mg_dL' in df.columns and 'Age' in df.columns and 'Sexe' in df.columns:
        gender_mult = df['Sexe'].astype(str).str.lower().apply(lambda x: 0.742 if 'f' in x else 1.0)
        # Avoid division by zero/negatives for power
        safe_creat = df['Creat_mg_dL'].clip(lower=0.1)
        safe_age = df['Age'].clip(lower=1)
        df['eGFR_MDRD'] = 175 * (safe_creat**-1.154) * (safe_age**-0.203) * gender_mult
        print("Features cliniques (eGFR, Ratio U/C) calculées.")

    # --- 3. Suppression Leakage ---
    leak_terms = ["Causes Majeure après Diagnostic", "Evolution de l'Etat Générale", "Diagnostic final"]
    cols_to_drop_leak = [c for c in df.columns if any(term in c for term in leak_terms)]
    df = df.drop(columns=cols_to_drop_leak)

    # --- 4. Encodage Ordinal ---
    ordinal_mappings = {
        'Hygiène buccodentaire': {'Mauvaise': 0, 'Insuffisante': 1, 'Acceptable': 2, 'Bonne': 3},
        'Conscience': {'Coma': 0, 'Obnubilé': 1, 'Somnolence': 2, 'Claire': 3},
        'Etat Général (EG) à l\'Admission': {'Altéré': 0, 'Urémique': 1, 'Acceptable': 2, 'Bon': 3}
    }
    for col, mapping in ordinal_mappings.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    # --- 5. Imputation & Scaling ---
    all_null_cols = df.columns[df.isnull().all()]
    df = df.drop(columns=all_null_cols)
    
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    if target_col in cat_cols: cat_cols.remove(target_col)
    if "ID" in cat_cols: cat_cols.remove("ID")

    if num_cols:
        mice_imputer = IterativeImputer(random_state=42, max_iter=10)
        df[num_cols] = mice_imputer.fit_transform(df[num_cols])
        joblib.dump(mice_imputer, 'artifacts/mice_imputer.joblib')

    if cat_cols:
        cat_imputer = SimpleImputer(strategy='most_frequent')
        df[cat_cols] = cat_imputer.fit_transform(df[cat_cols])
        joblib.dump(cat_imputer, 'artifacts/cat_imputer.joblib')

    # Encodage Cible
    le = LabelEncoder()
    df[target_col] = le.fit_transform(df[target_col])
    joblib.dump(le, 'artifacts/target_encoder.joblib')

    # One-Hot Encoding
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # Robust Scaling
    scaler = RobustScaler()
    features = df.drop(columns=[target_col, 'ID'], errors='ignore')
    
    # Nettoyage des noms de colonnes pour XGBoost (Pas de [, ], <)
    import re
    features.columns = [re.sub(r'[\[\]<]', '_', str(col)) for col in features.columns]
    
    scaled_features = scaler.fit_transform(features)
    joblib.dump(scaler, 'artifacts/scaler.joblib')

    # Export
    df_final = pd.DataFrame(scaled_features, columns=features.columns)
    df_final[target_col] = df[target_col].values
    df_final.to_csv('processed/ckd_processed.csv', index=False)
    print(f"Dataset final généré : {df_final.shape}")

if __name__ == "__main__":
    preprocess_data('../ckd_dataset.csv')
