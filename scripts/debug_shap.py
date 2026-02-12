import joblib
import pandas as pd
import numpy as np
import shap
from pathlib import Path

assets_path = Path("backend/model_assets")
model = joblib.load(assets_path / "model.joblib")
scaler = joblib.load(assets_path / "scaler.joblib")

# Données d'exemple (270 colonnes)
features = list(scaler.feature_names_in_)
X_dummy = pd.DataFrame(0.0, index=[0], columns=features)
X_scaled = scaler.transform(X_dummy)

print(f"Prediction: {model.predict(X_scaled)}")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_scaled)

print(f"Type of shap_values: {type(shap_values)}")
if isinstance(shap_values, list):
    print(f"List length: {len(shap_values)}")
    print(f"Shape of first element: {shap_values[0].shape}")
elif isinstance(shap_values, np.ndarray):
    print(f"Array shape: {shap_values.shape}")
else:
    print(f"Object: {shap_values}")
