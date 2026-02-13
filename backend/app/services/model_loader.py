import os
from huggingface_hub import hf_hub_download
from pathlib import Path
import shutil

# Configuration
REPO_ID = "username/renal-ai-models" # À REMPLACER PAR LE MEME REPO QUE UPLOAD
MODEL_DIR = Path(__file__).parent.parent.parent / "model_assets"
FILES_TO_DOWNLOAD = ["model.joblib", "scaler.joblib", "target_encoder.joblib"]

def load_models_from_hf():
    """
    Télécharge les modèles depuis Hugging Face Hub s'ils ne sont pas présents localement
    ou si on force la mise à jour.
    """
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    print(f"🔄 Vérification des modèles dans {MODEL_DIR}...")
    
    try:
        for filename in FILES_TO_DOWNLOAD:
            local_path = MODEL_DIR / filename
            if not local_path.exists():
                print(f"⬇️ Téléchargement confidentiel de {filename} depuis HF...")
                # On utilise hf_hub_download qui gère le cache automatiquement
                downloaded_path = hf_hub_download(
                    repo_id=REPO_ID,
                    filename=filename,
                    local_dir=MODEL_DIR,
                    local_dir_use_symlinks=False # Important pour Render/Heroku
                )
                print(f"✅ {filename} téléchargé.")
            else:
                print(f"✨ {filename} présent localement.")
                
    except Exception as e:
        print(f"⚠️ Attention : Impossible de télécharger les modèles depuis HF ({str(e)})")
        print("ℹ️ Le backend tentera d'utiliser les fichiers locaux existants.")

if __name__ == "__main__":
    load_models_from_hf()
