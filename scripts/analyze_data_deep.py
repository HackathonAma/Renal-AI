import pandas as pd
import os

df = pd.read_csv(r"c:\Users\HP\Desktop\Bootcamp AMA\ckd_dataset.csv")
cols = list(df.columns)

print(f"Total columns: {len(cols)}")

# Identify target candidates
target_candidates = [c for c in cols if any(word in c.lower() for word in ['stade', 'stage', 'ckd', 'maladie', 'score'])]
print("\n--- TARGET CANDIDATES ---")
print(target_candidates)

# Group columns by keywords
categorized = {
    "Sociodemographique": ['Sexe', 'Age', 'Profession', 'Departement', 'Commune'],
    "Medical History": ['HTA', 'Hypertension', 'Diabete', 'AVC', 'Cardiaque'],
    "Lifestyle": ['Tabac', 'Alcool', 'Sport', 'Alimentation'],
    "Biological": ['Creatinine', 'Uree', 'Albumine', 'Glycemie', 'Proteinurie', 'Hematurie'],
    "Physiological": ['Tension', 'Pouls', 'Diurese', 'Poids', 'Taille']
}

print("\n--- CATEGORIZED COLUMNS ---")
for cat, keywords in categorized.items():
    found = [c for c in cols if any(k.lower() in c.lower() for k in keywords)]
    print(f"{cat}: {found[:10]} ... ({len(found)} found)")

# Check unique values for the most likely target
if target_candidates:
    primary_target = target_candidates[0]
    print(f"\n--- VALUES FOR {primary_target} ---")
    print(df[primary_target].value_counts())
else:
    print("\nNo obvious target column found with keywords. Checking all columns for small discrete sets of values.")
    for c in cols:
        unique_count = df[c].nunique()
        if 2 <= unique_count <= 6:
            # Look for values like 'Stade 1', 'Stade 2', etc.
            sample_vals = df[c].unique()
            if any('stade' in str(v).lower() for v in sample_vals):
                print(f"Potential target column by values: {c} -> {sample_vals}")

# Look for GFR or DFGe (Estimated Glomerular Filtration Rate) as it's used to calculate stages
gfr_cols = [c for c in cols if any(k in c.lower() for k in ['dfg', 'gfr', 'clairance'])]
print("\n--- GFR/DFG COLUMNS ---")
print(gfr_cols)
