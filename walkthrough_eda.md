# Rapport d'Analyse Exploratoire des Données (EDA) Enrichi - CKD Prediction

Ce document présente les résultats détaillés de l'analyse exploratoire effectuée sur le dataset de la Maladie Rénale Chronique (CKD).

## 1. Vue d'ensemble du Dataset
- **Nombre de patients (lignes) :** 308
- **Nombre de caractéristiques (colonnes) :** 201
- **Qualité des données :** 87 colonnes ont été converties avec succès en types numériques (le reste étant des données textuelles/catégorielles ou très éparses).

## 2. Distribution des Stages de l'IRC
La distribution est relativement équilibrée entre les différents stades, ce qui est idéal pour l'entraînement d'un modèle de classification.

![Distribution de la cible](file:///c:/Users/HP/Desktop/Bootcamp%20AMA/models/plots/target_distribution.png)

## 3. Analyse des Corrélations (Insights Médicaux)
La matrice de corrélation ci-dessous montre les variables les plus liées au stade de l'IRC.

![Matrice de corrélation](file:///c:/Users/HP/Desktop/Bootcamp%20AMA/models/plots/correlation_matrix.png)

### Top 5 des prédicteurs numériques :
1. **Créatinine (mg/L) :** Corr. 0.59 - Indicateur clé de la fonction rénale.
2. **P (Phosphore meq/L) :** Corr. 0.58 - Les déséquilibres de phosphore sont fréquents en cas d'IRC.
3. **Symptômes/Asthénie :** Corr. 0.44 - Signe clinique fort.
4. **Symptômes/Vomissements :** Corr. 0.40 - Souvent lié à l'urémie.
5. **Symptômes/Insomnie :** Corr. 0.33.

## 4. Carte de Suture (Data Sparsity)
Le dataset présente une forte proportion de données manquantes dans certaines colonnes (jusqu'à 99%). Pour le modèle, nous devrons sélectionner les features ayant une densité suffisante ou utiliser des méthodes d'imputation robustes.

![Heatmap des manquants](file:///c:/Users/HP/Desktop/Bootcamp%20AMA/models/plots/missing_data_heatmap.png)

## 5. Conclusions et Prochaines Étapes
- **Variables Cliniques :** La Créatinine et le Phosphore seront des features primordiales.
- **Symptômes :** Plusieurs variables binaires (symptômes) montrent des signaux intéressants.
- **Action suivante :** Préprocessing (imputation des valeurs manquantes et encodage) en se concentrant sur les variables à fort signal.

---
*Rapport généré automatiquement par le script `models/eda.py` le 12 Février 2026.*
