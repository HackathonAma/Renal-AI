# Journal de Décision - Models

| Date | Décision / Étape | Justification / Raisonnement | Résultat / Impact |
| :--- | :--- | :--- | :--- |
| 2026-02-12 | Initialisation | Lancement du projet de modélisation CKD | Structure de dossiers créée |
| 2026-02-12 | Début de l'EDA | Analyse initiale du fichier `ckd_dataset.csv` pour comprendre la structure et les types de données. | Terminée (214 colonnes identifiées) |
| 2026-02-12 | Création script EDA | Développement d'un script `models/eda.py` pour une analyse statistique systématique. | Terminée |
| 2026-02-12 | Setup Environnement | Création d'un environnement virtuel (`venv`) et du fichier `requirements.txt`. | Terminée |
| 2026-02-12 | Gestion Dépendances | Centralisation des bibliothèques nécessaires (pandas, seaborn, fastapi, etc.). | Terminée |
| 2026-02-12 | Analyse Résultats EDA | Observation : Toutes les colonnes sont lues comme 'object'. Problème de format décimal (,) et données mixtes. | Terminée |
| 2026-02-12 | Raffinement EDA | Mise à jour de `eda.py` : conversion numérique robuste (87 colonnes), nettoyage de la cible ("0%"). | Terminée |
| 2026-02-12 | Analyse Corrélations | Créatinine (0.59) et Phosphore (0.58) identifiés comme corrélations majeures. | Terminée |
| 2026-02-12 | Matrice Corrélation | Génération de la heatmap des corrélations (Top 15 features). | Terminée |
| 2026-02-12 | Documentation Finale | Création du rapport enrichi `walkthrough_eda.md` dans la racine du projet. | Terminée |
| 2026-02-12 | Master Preprocessing | Abandon de SimpleImputer pour IterativeImputer (MICE) afin de préserver les liens Urée/Créatinine. | Terminée |
| 2026-02-12 | Mapping Ordinal | Encodage manuel de 'Conscience' et 'Hygiène' pour conserver le signal de sévérité. | Terminée |
| 2026-02-12 | Robust Scaling | Passage au RobustScaler pour protéger le signal contre les valeurs extrêmes en labo. | Terminée |
| 2026-02-12 | Nettoyage Sémantique | Fusion des synonymes ('Veuf'/'Veuf(ve)') et suppression du bruit textuel ('4%', '38%'). | Terminée |
| 2026-02-12 | Feature Engineering | Ajout de l'eGFR (MDRD) et du ratio Urée/Créatinine pour différencier les stages. | Terminée |
| 2026-02-12 | Modèles Robustes | Transition vers Random Forest pour sa meilleure généralisation sur petits datasets. | Terminée |
| 2026-02-12 | Atteinte Objectifs | F1-Score Macro remonté à 0.68 (vs 0.60 initial). Performance sur CKD 3b stabilisée. | Terminée |
| 2026-02-12 | Anti-Overfitting | Subsampling (0.8) et régularisation (L2=2) appliqués avec succès. | Terminée |
| 2026-02-12 | Début Modeling | Lancement de la phase d'entraînement multi-modèles (Classification multiclasse). | Terminée |
| 2026-02-12 | Sélection Algorithmes | Choix : XGBoost (optimisé par GridSearch). Performance supérieure à Random Forest. | Terminée |
| 2026-02-12 | Métrique de Succès | Précision de 92% sur le Stage 5 (critique). Macro F1-Score stable à ~60%. | Terminée |
| 2026-02-12 | Risk Scoring | Implémentation d'un algorithme de calcul de score de risque basé sur les probabilités de la classe 5. | Terminée |
| 2026-02-12 | Sauvegarde Modèle | Enregistrement de `best_model_xgboost.joblib` pour intégration Backend. | Terminée |
