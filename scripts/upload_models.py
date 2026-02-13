import os
import sys
from huggingface_hub import HfApi
from pathlib import Path

# Configuration
REPO_ID = "username/renal-ai-models" # À REMPLACER PAR VOTRE REPO HF
MODEL_DIR = Path("backend/model_assets")
HF_TOKEN = os.getenv("HF_TOKEN")

def upload_models():
    if not HF_TOKEN:
        print("❌ Erreur : Variable d'environnement HF_TOKEN manquante.")
        sys.exit(1)

    print(f"🚀 Démarrage de l'upload des modèles vers {REPO_ID}...")
    api = HfApi()

    try:
        # Création du repo s'il n'existe pas
        api.create_repo(repo_id=REPO_ID, exist_ok=True, repo_type="model")
        
        # Upload du dossier complet
        api.upload_folder(
            folder_path=MODEL_DIR,
            repo_id=REPO_ID,
            repo_type="model",
            commit_message=f"Auto-update models from GitHub Actions {os.getenv('GITHUB_SHA', '')[:7]}"
        )
        print("✅ Upload terminé avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de l'upload : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    upload_models()
