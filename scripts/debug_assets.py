import joblib
import pandas as pd
from pathlib import Path

assets_path = Path("backend/model_assets")
try:
    model = joblib.load(assets_path / "model.joblib")
    scaler = joblib.load(assets_path / "scaler.joblib")
    
    print("--- Model Information ---")
    if hasattr(model, "feature_names_in_"):
        print(f"Features expected by Model: {len(model.feature_names_in_)}")
        print(model.feature_names_in_[:10])
    
    print("\n--- Scaler Information ---")
    if hasattr(scaler, "feature_names_in_"):
        print(f"Features expected by Scaler: {len(scaler.feature_names_in_)}")
        # print(scaler.feature_names_in_[:10])
    
    if (assets_path / "selected_features.joblib").exists():
        selected = joblib.load(assets_path / "selected_features.joblib")
        print(f"\nSaved selected_features count: {len(selected)}")
    else:
        print("\nselected_features.joblib NOT FOUND")

except Exception as e:
    print(f"Error: {e}")
