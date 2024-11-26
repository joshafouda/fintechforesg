import pandas as pd
from src.scoring_functions import (
    calculate_mobile_money_scores,
    calculate_data_service_scores,
    calculate_voice_service_scores,
    calculate_sms_service_scores,
    calculate_digital_service_scores
)

def generate_profile_code(filtered_data):
    """
    Génère le profil final 'Profile_Code' en concaténant les scores de chaque service.

    Args:
        filtered_data (pd.DataFrame): DataFrame contenant les scores des différents services.

    Returns:
        pd.DataFrame: DataFrame enrichie avec la colonne 'Profile_Code'.
    """
    # Remplacer les valeurs manquantes par une chaîne vide avant la concaténation
    filtered_data['Profile_Code'] = (
        filtered_data['Mobile_Money_Score'].fillna(0).astype(int).astype(str) +
        filtered_data['Data_Service_Score'].fillna(0).astype(int).astype(str) +
        filtered_data['Voice_Service_Score'].fillna(0).astype(int).astype(str) +
        filtered_data['SMS_Service_Score'].fillna(0).astype(int).astype(str) +
        filtered_data['Digital_Service_Score'].fillna(0).astype(int).astype(str)
    )
    return filtered_data

if __name__ == "__main__":
    # Définir les chemins des fichiers
    filtered_data_path = "data/processed/filtered_data.csv"
    scored_data_path = "data/processed/scored_data.csv"

    # Charger les données pré-filtrées
    print("Chargement des données pré-filtrées...")
    filtered_data = pd.read_csv(filtered_data_path)

    # Calcul des scores Mobile Money
    print("Calcul des scores Mobile Money...")
    mobile_money_scores = calculate_mobile_money_scores(filtered_data)

    # Calcul des scores Data Service
    print("Calcul des scores Data Service...")
    data_service_scores = calculate_data_service_scores(filtered_data)

    # Calcul des scores Voice Service
    print("Calcul des scores Voice Service...")
    voice_service_scores = calculate_voice_service_scores(filtered_data)

    # Calcul des scores SMS Service
    print("Calcul des scores SMS Service...")
    sms_service_scores = calculate_sms_service_scores(filtered_data)

    # Calcul des scores Digital Service
    print("Calcul des scores Digital Service...")
    digital_service_scores = calculate_digital_service_scores(filtered_data)

    # Vérification des clés avant fusion
    print("Vérification des clés dans les DataFrames de scores...")
    for df, name in zip(
        [mobile_money_scores, data_service_scores, voice_service_scores, sms_service_scores, digital_service_scores],
        ["Mobile_Money_Score", "Data_Service_Score", "Voice_Service_Score", "SMS_Service_Score", "Digital_Service_Score"]
    ):
        if "SIM_NUMBER" not in df.columns:
            raise KeyError(f"La colonne 'SIM_NUMBER' est manquante dans {name}")

    # Mise à jour de filtered_data avec les scores
    print("Fusion des scores dans filtered_data...")
    filtered_data = filtered_data.merge(
        mobile_money_scores.rename(columns={"score": "Mobile_Money_Score"}), 
        on="SIM_NUMBER", how="left"
    )
    filtered_data = filtered_data.merge(
        data_service_scores.rename(columns={"score": "Data_Service_Score"}), 
        on="SIM_NUMBER", how="left"
    )
    filtered_data = filtered_data.merge(
        voice_service_scores.rename(columns={"score": "Voice_Service_Score"}), 
        on="SIM_NUMBER", how="left"
    )
    filtered_data = filtered_data.merge(
        sms_service_scores.rename(columns={"score": "SMS_Service_Score"}), 
        on="SIM_NUMBER", how="left"
    )
    filtered_data = filtered_data.merge(
        digital_service_scores.rename(columns={"score": "Digital_Service_Score"}), 
        on="SIM_NUMBER", how="left"
    )

    # Vérifier les colonnes avant de générer le Profile_Code
    print("Colonnes disponibles avant Profile_Code :")
    print(filtered_data.columns)

    # Générer le Profile_Code
    print("Génération du Profile_Code...")
    scored_data = generate_profile_code(filtered_data)

    # Sauvegarder les résultats
    print(f"Sauvegarde des données scorées dans {scored_data_path}...")
    scored_data.to_csv(scored_data_path, index=False)
    print(f"Données scorées sauvegardées dans {scored_data_path}")
