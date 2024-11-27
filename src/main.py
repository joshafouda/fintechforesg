import os
import pandas as pd
from src.data_simulation import simulate_data
from src.data_processing import load_and_merge_data
from src.data_filtering import filter_data
from src.scoring_and_profiling import calculate_all_scores, generate_profile_code
from src.segmentation import segment_profiles
from src.cash_allocation import calculate_individual_credits, calculate_business_credits

def main():
    # Définir les chemins des fichiers
    base_path = os.getcwd()
    raw_data_path = os.path.join(base_path, "data", "raw")
    processed_data_path = os.path.join(base_path, "data", "processed")
    
    user_data_path = os.path.join(raw_data_path, "simulated_USER_DATA_with_dates.csv")
    kyc_data_path = os.path.join(raw_data_path, "simulated_KYC_DATA.csv")
    merged_data_path = os.path.join(processed_data_path, "merged_data.csv")
    filtered_data_path = os.path.join(processed_data_path, "filtered_data.csv")
    scored_data_path = os.path.join(processed_data_path, "scored_data.csv")
    segmented_data_path = os.path.join(processed_data_path, "segmented_data.csv")
    cash_allocated_data_path = os.path.join(processed_data_path, "cash_allocated_data.csv")
    
    # Étape 1 : Simulation des données
    print("Étape 1 : Simulation des données...")
    simulate_data(raw_data_path)
    print(f"Données simulées sauvegardées dans {raw_data_path}")
    
    # Étape 2 : Fusion des données
    print("Étape 2 : Fusion des données...")
    merged_data = load_and_merge_data(user_data_path, kyc_data_path)
    merged_data.to_csv(merged_data_path, index=False)
    print(f"Fichier fusionné sauvegardé dans {merged_data_path}")
    
    # Étape 3 : 
    print("Étape 3 : Veuillez exécuter le Notebook EDA dans notebooks/EDA_merged_data.ipynb.")

    # Étape 4 : Pré-filtration des données clients
    print("Étape 4 : Pré-filtration des données clients...")
    filtered_data = filter_data(merged_data)
    filtered_data.to_csv(filtered_data_path, index=False)
    print(f"Fichier filtré sauvegardé dans {filtered_data_path}")

    # Étape 5 : Rappel pour l'EDA sur filtered_data
    print("Étape 5 : Veuillez exécuter le Notebook EDA dans notebooks/EDA_filtered_data.ipynb.")
    
    # Étape 6 : Scoring et génération des profils
    try:
        print("Étape 6 : Calcul des scores et génération des profils...")
        filtered_data = calculate_all_scores(filtered_data)
        scored_data = generate_profile_code(filtered_data)

        # Sauvegarde des données scorées
        scored_data.to_csv(scored_data_path, index=False)
        print(f"Fichier scoré sauvegardé dans {scored_data_path}")

    except Exception as e:
        print(f"Erreur lors de l'étape 6 : {e}")
        print("Veuillez vérifier scoring_and_profiling.py pour diagnostiquer le problème.")

    # Étape 7 : Analyse exploratoire des résultats de scoring et de profiling
    print("Étape 7 : Veuillez exécuter le Notebook EDA dans notebooks/EDA_scored_data.ipynb.")

    # Étape 8 : Segmentation des profils
    print("Étape 8 : Segmentation des profils...")
    try:
        scored_data = pd.read_csv(scored_data_path)
        segmented_data = segment_profiles(scored_data)
        segmented_data.to_csv(segmented_data_path, index=False)
        print(f"Données segmentées sauvegardées dans {segmented_data_path}")
    except Exception as e:
        print(f"Erreur lors de l'étape 8 : {e}")
        print("Veuillez vérifier segmentation.py pour diagnostiquer le problème.")

    # Étape 9 : Analyse des segments
    print("Étape 9 : Veuillez exécuter le Notebook EDA dans notebooks/EDA_segments.ipynb.")

    # Étape 10 : Attribution des crédits
    print("Étape 10 : Attribution des crédits...")
    try:
        segmented_data = pd.read_csv(segmented_data_path)

        # Appliquer les fonctions d'attribution
        segmented_data[['Nano_Loan', 'Advanced_Credit']] = segmented_data.apply(
            calculate_individual_credits, axis=1, result_type='expand'
        )
        segmented_data[['Macro_Loan', 'Cash_Roller_Over']] = segmented_data.apply(
            calculate_business_credits, axis=1, result_type='expand'
        )

        # Sauvegarder les résultats
        segmented_data.to_csv(cash_allocated_data_path, index=False)
        print(f"Données avec crédits sauvegardées dans {cash_allocated_data_path}")
    except Exception as e:
        print(f"Erreur lors de l'étape 10 : {e}")
        print("Veuillez vérifier cash_allocation.py pour diagnostiquer le problème.")

    # Étape 11 : Analyse des crédits alloués
    print("Étape 11 : Veuillez exécuter le Notebook EDA dans notebooks/EDA_cash_allocated.ipynb.")

    
    
    print("Pipeline exécuté avec succès !")

if __name__ == "__main__":
    main()
