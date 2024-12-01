### **Mise à Jour du `README.md`**

---

# FinTech for ESG

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

- **`notebooks/`** :
  - Notebooks interactifs pour l'analyse exploratoire des données :
    - `EDA_merged_data.ipynb` : Analyse des données fusionnées.
    - `EDA_filtered_data.ipynb` : Analyse des données après pré-filtration.
    - `EDA_scored_data.ipynb` : Analyse des résultats de scoring et profiling.
    - `EDA_segments.ipynb` : Analyse des segments générés à partir des profils.

- **`src/`** :
  - Contient les scripts principaux pour la simulation, le traitement et l'analyse des données :
    - `data_simulation.py` : Génération des données simulées.
    - `data_processing.py` : Fusion des données utilisateur et KYC.
    - `data_filtering.py` : Pré-filtration des données pour obtenir une base propre.
    - `scoring_and_profiling.py` : Calcul des scores et génération des profils.
    - `segmentation.py` : Segmentation des profils en groupes (Very High, High, etc.).
    - `bonus_malus_calculation.py` : (placeholder pour les calculs des bonus/malus).

- **`tests/`** :
  - Tests unitaires pour valider les fonctions principales :
    - `test_data_processing.py` : Tests pour la fusion des données.
    - `test_data_filtering.py` : Tests pour la pré-filtration des données.
    - `test_scoring_and_profiling.py` : Tests pour le calcul des scores et profils.
    - `test_segmentation.py` : Tests pour la segmentation des profils.

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
python src/main.py
```

### **2. Exécution Étape par Étape**

Si vous souhaitez exécuter des étapes spécifiques, voici les commandes associées :

#### **Simulation des Données**

Génère les fichiers simulés dans `data/raw/` :

```bash
python src/data_simulation.py
```

#### **Fusion des Données**

Fusionne les fichiers utilisateur et KYC, et sauvegarde `merged_data.csv` dans `data/processed/` :

```bash
python src/data_processing.py
```

#### **Pré-filtration des Données**

Filtre les données fusionnées pour obtenir une base propre :

```bash
python src/data_filtering.py
```

#### **Calcul des Scores et Génération des Profils**

Calcule les scores des différents services, génère les profils et sauvegarde `scored_data.csv` dans `data/processed/` :

```bash
python src/scoring_and_profiling.py
```

#### **Segmentation des Profils**

Segmente les profils en cinq groupes (`Very High`, `High`, `Medium`, `Low`, `Very Low`) et sauvegarde `segmented_data.csv` dans `data/processed/` :

```bash
python src/segmentation.py
```

### **3. Analyse Exploratoire avec les Notebooks**
Pour explorer les différentes étapes des données, ouvrez les notebooks correspondants dans le dossier `notebooks/` :

- **Fusion des Données** : `EDA_merged_data.ipynb`              
- **Pré-filtration** : `EDA_filtered_data.ipynb`                   
- **Scoring et Profiling** : `EDA_scored_data.ipynb`                   
- **Segmentation des Profils** : `EDA_segments.ipynb`                          

Exécutez-les avec :

```bash
jupyter notebook
```
ou de manière interactive au sein du notebook (exécution de chaque cellule)

### **4. Tester les Fonctions**

Pour exécuter les tests unitaires et vérifier la robustesse des fonctions, utilisez :

```bash
pytest tests/
```
Les tests incluent :

- Fusion des données.                       
- Pré-filtration des données.                       
- Calcul des scores et des profils.                     
- Segmentation des profils.                         


---

## **Analyse Exploratoire**

Les analyses exploratoires sont réalisées dans les Notebooks suivants :

1. **EDA sur `merged_data`** :

   Analyse des données fusionnées, leur structure, et leurs caractéristiques globales.

   Ouvrez et exécutez le Notebook :

   ```bash
   notebooks/EDA_merged_data.ipynb
   ```

2. **EDA sur `filtered_data`** :

   Analyse des données après pré-filtration pour comprendre les distributions et les attributs des clients retenus.

   Ouvrez et exécutez le Notebook :

   ```bash
   notebooks/EDA_filtered_data.ipynb
   ```

3. **EDA sur `scored_data`** :

   Exploration des scores calculés pour chaque service (Mobile Money, Data, Voice, SMS, Digital) et des profils générés.

   Ouvrez et exécutez le Notebook :

   ```bash
   notebooks/EDA_scored_data.ipynb
   ```

4. **EDA sur les Segments** :

   Analyse des segments (`Very High`, `High`, `Medium`, `Low`, `Very Low`) générés à partir des profils et des scores pondérés.

   Ouvrez et exécutez le Notebook :

   ```bash
   notebooks/EDA_segments.ipynb
   ```

### **Instructions pour Exécuter les Notebooks**

Pour exécuter les Notebooks, utilisez la commande suivante dans votre terminal :

```bash
jupyter notebook
```
Ensuite, naviguez jusqu'au fichier Notebook que vous souhaitez explorer et exécutez les cellules.


---

## **Tests**

Pour exécuter les tests unitaires et valider le bon fonctionnement des fonctions principales :

### **Commandes**

1. **Exécution de tous les tests** :

   Pour lancer l'ensemble des tests dans le répertoire `tests/` :

   ```bash
   python -m unittest discover tests
   ```

2. **Exécution avec Pytest** (optionnel, si installé) :

   Vous pouvez également utiliser `pytest` pour exécuter les tests avec des rapports plus détaillés :

   ```bash
   pytest tests/
   ```

### **Tests Disponibles**

Les tests couvrent les principales étapes du pipeline :

- **Fusion des données** : Valide la combinaison des fichiers utilisateur et KYC.

- **Pré-filtration** : Vérifie que les critères de sélection des clients sont correctement appliqués.

- **Calcul des scores et profils** : Assure la cohérence des scores pour chaque service et des profils générés.

- **Segmentation des profils** : Valide le calcul des scores pondérés et l'attribution des segments.

Pour exécuter un test spécifique :

```bash
python -m unittest tests.test_nom_du_fichier
```

---

## **Prochaines Étapes**
1. Intégration des calculs de bonus/malus.
2. Ajout de visualisations avancées dans les Notebooks.
3. Mise en place d’un modèle de scoring pour les clients.

---

## **Auteurs**
- [Adresse Équipe](mailto:votre.email@example.com)

---

### **Instructions**
1. Remplacez `https://github.com/your-repo/fintechforesg.git` par le vrai lien de votre dépôt GitHub.
2. Ajoutez ou modifiez des sections si de nouvelles étapes sont intégrées.

