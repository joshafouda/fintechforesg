import numpy as np
import pandas as pd
import os

def segment_profiles(scored_data):
    """
    Segmente les profils en cinq catégories (Very High, High, Medium, Low, Very Low)
    en fonction du score pondéré calculé à partir de Profile_Code.

    Args:
        scored_data (pd.DataFrame): Données scorées contenant la colonne 'Profile_Code'.

    Returns:
        pd.DataFrame: Données enrichies avec les colonnes 'Weighted_Score' et 'Segment'.
    """

    # Calculer le score pondéré pour chaque Profile_Code
    def calculate_weighted_score(profile_code):
        weights = {
            'Mobile Money': 5,
            'Data': 4,
            'Voice': 3,
            'SMS': 2,
            'Digital': 1
        }
        mobile_money_score = int(str(profile_code)[0]) * weights['Mobile Money']
        data_score = int(str(profile_code)[1]) * weights['Data']
        voice_score = int(str(profile_code)[2]) * weights['Voice']
        sms_score = int(str(profile_code)[3]) * weights['SMS']
        digital_score = int(str(profile_code)[4]) * weights['Digital']

        return mobile_money_score + data_score + voice_score + sms_score + digital_score

    print("Calcul des scores pondérés...")
    scored_data['Weighted_Score'] = scored_data['Profile_Code'].apply(calculate_weighted_score)

    # Calculer les percentiles pour la segmentation
    percentiles = np.percentile(scored_data['Weighted_Score'], [20, 40, 60, 80])

    # Fonction pour catégoriser en fonction des percentiles
    def categorize_by_percentile(weighted_score):
        if weighted_score >= percentiles[3]:  # Au-dessus du 80e percentile
            return 'Very High'
        elif weighted_score >= percentiles[2]:  # Entre 60e et 80e percentile
            return 'High'
        elif weighted_score >= percentiles[1]:  # Entre 40e et 60e percentile
            return 'Medium'
        elif weighted_score >= percentiles[0]:  # Entre 20e et 40e percentile
            return 'Low'
        else:  # En dessous du 20e percentile
            return 'Very Low'

    print("Catégorisation des segments...")
    scored_data['Segment'] = scored_data['Weighted_Score'].apply(categorize_by_percentile)

    return scored_data


if __name__ == "__main__":
    
    # Définir les chemins des fichiers
    base_path = os.getcwd()
    processed_data_path = os.path.join(base_path, "data", "processed")
    scored_data_path = os.path.join(processed_data_path, "scored_data.csv")
    segmented_data_path = os.path.join(processed_data_path, "segmented_data.csv")

    # Charger les données scorées
    print("Chargement des données scorées...")
    scored_data = pd.read_csv(scored_data_path)

    # Appliquer la segmentation
    from src.segmentation import segment_profiles
    segmented_data = segment_profiles(scored_data)

    # Vérifier la présence de la colonne "Segment"
    if "Segment" in segmented_data.columns:
        print("La colonne 'Segment' a été créée avec succès.")
        print("Modalités uniques de 'Segment' :")
        print(segmented_data["Segment"].unique())
    else:
        print("Erreur : La colonne 'Segment' n'a pas été créée.")
        raise ValueError("La colonne 'Segment' est manquante dans les données segmentées.")

    # Sauvegarder les données segmentées
    print(f"Sauvegarde des données segmentées dans {segmented_data_path}...")
    segmented_data.to_csv(segmented_data_path, index=False)
    print("Segmentation terminée avec succès.")

