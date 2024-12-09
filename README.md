# FINTECH4ESG

## **Description**
Ce projet vise à développer un système d'analyse, de pré-filtration et de scoring pour des clients de Mobile Money, en se basant sur leurs données d'utilisation et leur conformité KYC (Know Your Customer).

---

## **Structure du Projet**

- **`data/`** :

  - **`raw/`** : Contient les données brutes simulées, comme `simulated_USER_DATA_with_dates.csv` et `simulated_KYC_DATA.csv`.

  - **`processed/`** : Contient les fichiers de données intermédiaires ou résultats après traitement :

    - `merged_data.csv` : Données fusionnées.

    - `filtered_data.csv` : Données après pré-filtration.

    - `scored_data.csv` : Données avec les scores calculés.

    - `segmented_data.csv` : Données segmentées selon les scores pondérés.

    - `cash_allocated_data.csv` : Données avec crédits attribués aux clients.

    - `final_clients.csv` : Données finales après gestion des clients multi-SIM.

    - `transactions_previous_month.csv` : Transactions du 15 et dernier jour des mois précédents pour chaque client.

    - `final_clients_with_bonus_malus.csv` : Données finales enrichies avec les bonus/malus calculés.

    - `final_clients_with_updated_loans.csv` : Données finales avec les prêts mis à jour après application des bonus/malus.


- **`notebooks/`** :

  - Notebooks interactifs pour l'analyse exploratoire des données :

    - `EDA_merged_data.ipynb` : Analyse des données fusionnées.

    - `EDA_filtered_data.ipynb` : Analyse des données après pré-filtration.

    - `EDA_scored_data.ipynb` : Analyse des résultats de scoring et profiling.

    - `EDA_segments.ipynb` : Analyse des segments générés à partir des profils.

    - `EDA_cash_allocated.ipynb` : Analyse des crédits attribués aux clients (Nano Loan, Advanced Credit, etc.).

    - `EDA_bonus_malus_updated_loans.ipynb` : Analyse des bonus/malus et des montants de crédits mis à jour, reflétant la capacité de remboursement.


- **`src/`** :

  - Contient les scripts principaux pour la simulation, le traitement et l'analyse des données :

    - `data_simulation.py` : Génération des données simulées pour les utilisateurs, les KYC et les transactions.

    - `data_processing.py` : Fusion des données utilisateur et KYC pour créer un fichier consolidé.

    - `data_filtering.py` : Pré-filtration des données pour isoler les utilisateurs actifs et pertinents.

    - `scoring_and_profiling.py` : Calcul des scores pour les différents services (Mobile Money, Data, etc.) et génération des profils.

    - `segmentation.py` : Segmentation des profils en groupes (Very High, High, Medium, Low, Very Low) basés sur des scores pondérés.

    - `cash_allocation.py` : Attribution des crédits (Nano Loan, Macro Loan, etc.) aux clients, selon leur profil et catégorie.

    - `multi_sim_management.py` : Gestion des clients possédant plusieurs SIM et consolidation des profils.

    - `bonus_malus_calculation.py` : Implémentation des bonus/malus pour ajuster les prêts en fonction de la capacité de remboursement.

    - `main.py` : Point d'entrée unique pour exécuter l'ensemble du pipeline.


- **`tests/`** :

  - Tests unitaires pour valider les fonctions principales :

    - `test_data_processing.py` : Tests pour la fusion des données.

    - `test_data_filtering.py` : Tests pour la pré-filtration des données.


- **`main.py`** :

  - Point d'entrée unique pour exécuter l'ensemble du pipeline, de la simulation des données à la segmentation finale.

---

## **Installation**

### **1. Cloner le Projet**

```bash
git clone https://github.com/your-repo/fintechforesg.git

cd fintechforesg
```

### **2. Installer les Dépendances**

Assurez-vous d’avoir Python 3.7 ou une version ultérieure. Installez les bibliothèques nécessaires :

```bash
pip install -r requirements.txt
```

---

## **Utilisation**

### **1. Exécuter le Pipeline Complet**

Pour exécuter tout le projet, de la simulation des données aux résultats finaux, utilisez :

```bash
python3 src/main.py
```

### **2. Exécution Étape par Étape**

Si vous souhaitez exécuter des étapes spécifiques, voici les commandes associées :

#### **Simulation des Données**

Génère les fichiers simulés dans `data/raw/` :

```bash
python3 src/data_simulation.py
```

#### **Fusion des Données**

Fusionne les fichiers utilisateur et KYC, et sauvegarde `merged_data.csv` dans `data/processed/` :

```bash
python3 src/data_processing.py
```

#### **Pré-filtration des Données**

Filtre les données fusionnées pour obtenir une base propre :

```bash
python3 src/data_filtering.py
```

#### **Calcul des Scores et Génération des Profils**

Calcule les scores des différents services, génère les profils et sauvegarde `scored_data.csv` dans `data/processed/` :

```bash
python3 src/scoring_and_profiling.py
```

#### **Segmentation des Profils**

Segmente les profils en cinq groupes (`Very High`, `High`, `Medium`, `Low`, `Very Low`) et sauvegarde `segmented_data.csv` dans `data/processed/` :

```bash
python3 src/segmentation.py
```

### **3. Analyse Exploratoire avec les Notebooks**

Pour explorer les différentes étapes d'anañyse exploratoire des données, ouvrez les notebooks correspondants dans le dossier `notebooks/` :

- **Fusion des Données** : `EDA_merged_data.ipynb`

- **Pré-filtration** : `EDA_filtered_data.ipynb`

- **Scoring et Profiling** : `EDA_scored_data.ipynb`

- **Segmentation des Profils** : `EDA_segments.ipynb`

- etc.

Exécutez-les de manière interactive au sein du notebook (exécution de chaque cellule)

## **Auteurs**

- [Josué AFOUDA (Data Scientist)](afouda.josue@gmail.com)

- [Blaise](adresse@example.com)

- [JJ Bwanga](jjb@fintech4esg.com)

---

