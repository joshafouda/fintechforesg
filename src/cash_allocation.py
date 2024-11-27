import pandas as pd
import os

def calculate_individual_credits(row):
    """
    Calcule les crédits Nano et Advanced pour les clients individuels.

    Args:
        row (pd.Series): Ligne contenant les informations du client.

    Returns:
        tuple: (Nano Loan, Advanced Credit) pour les clients individuels.
    """
    # Extract profile code and category
    profile_code = str(row['Profile_Code'])
    category = row['CUST_CATEGORY']

    # Only calculate for Individual clients
    if category != "Individual":
        return None, None  # Return None for non-Individual clients

    # Définir les poids pour chaque service
    weights = [5, 4, 3, 2, 1]  # Mobile Money, Data, Voice, SMS, Digital

    # Calculer le score pondéré
    weighted_score = sum(int(digit) * weight for digit, weight in zip(profile_code, weights))

    # Plage de score pondéré
    min_score, max_score = 15, 75

    # Define Nano Loan and Advanced Credit ranges
    nano_min, nano_max = 20, 45
    advanced_min, advanced_max = 100, 500

    # Scale weighted_score within the actual range (15 to 75)
    normalized_score = (weighted_score - min_score) / (max_score - min_score)

    # Calculate Nano Loan and Advanced Credit based on the normalized score
    nano_loan = nano_min + normalized_score * (nano_max - nano_min)
    advanced_credit = advanced_min + normalized_score * (advanced_max - advanced_min)

    return nano_loan, advanced_credit


def calculate_business_credits(row):
    """
    Calcule les crédits Macro et Cash Roller Over pour les clients Business.

    Args:
        row (pd.Series): Ligne contenant les informations du client.

    Returns:
        tuple: (Macro Loan, Cash Roller Over) pour les clients Business.
    """
    # Extract profile code and category
    profile_code = str(row['Profile_Code'])
    category = row['CUST_CATEGORY']

    # Only calculate for Business clients
    if category != "Business":
        return None, None  # Return None for non-Business clients

    # Définir les poids pour chaque service
    weights = [5, 4, 3, 2, 1]  # Mobile Money, Data, Voice, SMS, Digital

    # Calculer le score pondéré
    weighted_score = sum(int(digit) * weight for digit, weight in zip(profile_code, weights))

    # Plage de score pondéré
    min_score, max_score = 15, 75

    # Define Macro Loan and Cash Roller Over ranges
    macro_min, macro_max = 25, 250
    cash_roller_min, cash_roller_max = 100, 500

    # Scale weighted_score within the actual range (15 to 75)
    normalized_score = (weighted_score - min_score) / (max_score - min_score)

    # Calculate Macro Loan based on the normalized score
    macro_loan = macro_min + normalized_score * (macro_max - macro_min)
    cash_roller = cash_roller_min + normalized_score * (cash_roller_max - cash_roller_min)

    return macro_loan, cash_roller


if __name__ == "__main__":
    
    # Définir les chemins des fichiers
    base_path = os.getcwd()
    processed_data_path = os.path.join(base_path, "data", "processed")
    segmented_data_path = os.path.join(processed_data_path, "segmented_data.csv")
    cash_allocated_data_path = os.path.join(processed_data_path, "cash_allocated_data.csv")

    # Charger les données segmentées
    print("Chargement des données segmentées...")
    segmented_data = pd.read_csv(segmented_data_path)

    # Appliquer les fonctions de calcul des crédits
    print("Calcul des crédits pour les clients individuels...")
    segmented_data[['Nano_Loan', 'Advanced_Credit']] = segmented_data.apply(
        calculate_individual_credits, axis=1, result_type='expand'
    )

    print("Calcul des crédits pour les clients Business...")
    segmented_data[['Macro_Loan', 'Cash_Roller_Over']] = segmented_data.apply(
        calculate_business_credits, axis=1, result_type='expand'
    )

    # Vérification des colonnes
    print("Vérification des crédits attribués...")
    credit_columns = ['Nano_Loan', 'Advanced_Credit', 'Macro_Loan', 'Cash_Roller_Over']
    missing_columns = [col for col in credit_columns if col not in segmented_data.columns]

    if missing_columns:
        print(f"Erreur : Les colonnes suivantes sont manquantes après attribution des crédits : {missing_columns}")
        raise ValueError("Attribution des crédits incomplète.")
    else:
        print("Toutes les colonnes de crédits sont présentes.")

    # Sauvegarder les données avec crédits
    print(f"Sauvegarde des données avec crédits dans {cash_allocated_data_path}...")
    segmented_data.to_csv(cash_allocated_data_path, index=False)
    print("Attribution des crédits terminée avec succès.")
