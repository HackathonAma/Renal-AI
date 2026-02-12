import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Configuration des graphiques
plt.style.use('ggplot')
os.makedirs('plots', exist_ok=True)

def perform_eda(file_path):
    print(f"Chargement du dataset : {file_path}")
    df = pd.read_csv(file_path)
    
    # 1. Nettoyage de la cible
    target_col = "Stage de l'IRC"
    if target_col in df.columns:
        print(f"\n--- Nettoyage de la cible ({target_col}) ---")
        df = df[df[target_col] != "0%"]
        print(f"Lignes restantes : {len(df)}")
    
    # 2. Conversion des types améliorée
    print("\n--- Conversion des types numériques (robustesse) ---")
    for col in df.columns:
        if col == target_col or col == "ID": continue
        
        # Nettoyage des chaînes
        temp = df[col].astype(str).str.strip().str.replace(',', '.', regex=False)
        # Tentative de conversion forcée (les erreurs deviennent NaN)
        converted = pd.to_numeric(temp, errors='coerce')
        
        # On garde la conversion si au moins 20% des valeurs sont devenues numériques
        if converted.notnull().sum() > 0.2 * len(df):
            df[col] = converted
            print(f"Convertie : {col} ({converted.notnull().sum()} valeurs numériques)")

    num_cols = df.select_dtypes(include=['number']).columns
    print(f"Nombre de colonnes numériques FINAL : {len(num_cols)}")
    
    # 3. Visualisation des données manquantes
    print("\n--- Génération de la heatmap des manquants ---")
    plt.figure(figsize=(15, 10))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
    plt.title("Carte des valeurs manquantes (Sparsity Map)")
    plt.tight_layout()
    plt.savefig('plots/missing_data_heatmap.png')
    print("Heatmap sauvegardée : plots/missing_data_heatmap.png")
    
    # 4. Visualisation des corrélations (Heatmap)
    print("\n--- Génération de la matrice de corrélation ---")
    if len(num_cols) > 1:
        df_temp = df.copy()
        df_temp[target_col] = df_temp[target_col].astype('category').cat.codes
        
        # On prend les 15 variables les plus corrélées (en valeur absolue) pour la lisibilité
        corr_matrix = df_temp[num_cols.tolist() + [target_col]].corr()[target_col].abs().sort_values(ascending=False)
        top_features = corr_matrix.head(15).index
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(df_temp[top_features].corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Matrice de Corrélation (Top 15 features)")
        plt.tight_layout()
        plt.savefig('plots/correlation_matrix.png')
        print("Matrice de corrélation sauvegardée : plots/correlation_matrix.png")

    # 5. Statistiques descriptives
    desc = df.describe().T

    # 6. Export des statistiques
    stats_file = "eda_statistics.txt"
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT EDA FINAL - {pd.Timestamp.now()}\n")
        f.write(f"Dimensions : {df.shape}\n")
        f.write(f"Colonnes numériques : {len(num_cols)}\n")
        f.write(f"\nDISTRIBUTION CIBLE :\n{df[target_col].value_counts().to_string()}\n")
        f.write("\nTOP CORRELATIONS (si possible) :\n")
        if len(num_cols) > 1:
            df_temp = df.copy()
            df_temp[target_col] = df_temp[target_col].astype('category').cat.codes
            corr = df_temp[num_cols.tolist() + [target_col]].corr()[target_col].sort_values(ascending=False)
            f.write(corr.head(20).to_string())
        
        f.write("\n\nSTATISTIQUES DESCRIPTIVES :\n")
        f.write(desc.to_string())
        
        missing = df.isnull().sum()
        f.write("\n\nVALEURS MANQUANTES (>30%) :\n")
        f.write(missing[missing > 0.3 * len(df)].sort_values(ascending=False).to_string())

    print(f"Rapport détaillé mis à jour : {stats_file}")

if __name__ == "__main__":
    perform_eda('../ckd_dataset.csv')

if __name__ == "__main__":
    perform_eda('../ckd_dataset.csv')
