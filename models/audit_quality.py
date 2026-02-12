import pandas as pd
import numpy as np

def audit_preprocessing(raw_path, processed_path):
    print("--- Audit Qualité du Préprocessing ---")
    raw = pd.read_csv(raw_path)
    processed = pd.read_csv(processed_path)
    
    # 1. Vérification des fuites (Data Leakage)
    if 'ID' in processed.columns:
        print("ALERTE : La colonne 'ID' est encore présente dans le dataset traité.")
    else:
        print("OK : La colonne 'ID' a été correctement retirée.")
        
    # 2. Vérification des corrélations extrêmes (Indication de fuite)
    target = "Stage de l'IRC"
    corrs = processed.corr()[target].abs().sort_values(ascending=False)
    if any(corrs[1:] > 0.95):
        print(f"ATTENTION : Fuite potentielle détectée (Corrélation > 0.95) :\n{corrs[corrs > 0.95]}")
    else:
        print("OK : Pas de corrélation suspecte (>0.95) avec la cible.")

    # 3. Analyse de la Sparsité des features conservées
    print(f"\nDimensions finales : {processed.shape}")
    print(f"Colonnes avec des valeurs nulles : {processed.isnull().sum().sum()}")
    
    # 4. Vérification de la diversité catégorielle
    # On regarde si des colonnes One-Hot ont une variance nulle
    low_variance = [col for col in processed.columns if processed[col].std() < 0.01]
    if low_variance:
        print(f"INFO : {len(low_variance)} colonnes ont une variance quasi-nulle (peu informatives).")

if __name__ == "__main__":
    audit_preprocessing('../ckd_dataset.csv', 'processed/ckd_processed.csv')
