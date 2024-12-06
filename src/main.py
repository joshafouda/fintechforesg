import os
import pandas as pd
from src.data_simulation import simulate_data
from src.data_processing import load_and_merge_data
from src.data_filtering import filter_data
from src.scoring_and_profiling import calculate_all_scores, generate_profile_code
from src.segmentation import segment_profiles
from src.cash_allocation import calculate_individual_credits, calculate_business_credits
from src.multi_sim_management import manage_multi_sim_clients, validate_final_clients
from src.bonus_malus_calculation import process_transactions, update_transactions, calculate_bonus_malus, update_loans_with_bonus_malus

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
    final_clients_path = os.path.join(processed_data_path, "final_clients.csv")

    transactions_file = os.path.join(raw_data_path, "real_transactions_with_dates.csv")
    final_clients_file = os.path.join(processed_data_path, "final_clients.csv")
    transactions_previous_month_file = os.path.join(processed_data_path, "transactions_previous_month.csv")
    final_clients_with_bonus_malus_file = os.path.join(processed_data_path, "final_clients_with_bonus_malus.csv")
    final_clients_with_updated_loans_file = os.path.join(processed_data_path, "final_clients_with_updated_loans.csv")
    
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


    # Étape 12 : Gestion des clients avec plusieurs SIM
    print("Étape 12 : Gestion des clients avec plusieurs SIM...")
    try:
        cash_allocated_data = pd.read_csv(cash_allocated_data_path)
        final_clients = manage_multi_sim_clients(cash_allocated_data)
        validate_final_clients(final_clients)
        final_clients.to_csv(final_clients_path, index=False)
        print(f"Données finales sauvegardées dans {final_clients_path}")
    except Exception as e:
        print(f"Erreur lors de l'étape 12 : {e}")
        print("Veuillez vérifier multi_sim_management.py pour diagnostiquer le problème.")

    
    # Étape 13 : Implémentation des bonus/malus
    try:
        print("Étape 13 : Implémentation des bonus/malus...")

        # Étape a: Créer le DataFrame des transactions pour le mois précédent
        print("Traitement des transactions pour le mois précédent...")
        process_transactions(transactions_file, transactions_previous_month_file)

        # Étape b: Mise à jour des transactions avec les informations des clients finaux
        print("Mise à jour des transactions avec les données des clients finaux...")
        update_transactions(
            transactions_previous_month_file,
            final_clients_file,
            transactions_previous_month_file
        )

        # Étape c: Calcul des bonus/malus
        print("Calcul des bonus/malus pour les clients...")
        calculate_bonus_malus(
            transactions_previous_month_file,
            final_clients_file,
            final_clients_with_bonus_malus_file
        )

        # Étape d: Mise à jour des prêts des clients avec le bonus/malus
        print("Mise à jour des prêts des clients avec le bonus/malus...")
        update_loans_with_bonus_malus(
            final_clients_with_bonus_malus_file,
            final_clients_with_updated_loans_file
        )

        print(f"Fichiers mis à jour avec succès dans {processed_data_path}.")

    except Exception as e:
        print(f"Erreur lors de l'étape 13 : {e}")

    
    # Étape 14 : Rappel pour l'analyse exploratoire des Bonus/Malus et des Montants de Crédits Mis à Jour
    print("Étape 14 : Veuillez exécuter le Notebook EDA dans notebooks/EDA_bonus_malus_updated_loans.ipynb.")



    print("Pipeline exécuté avec succès !")

if __name__ == "__main__":
    main()
