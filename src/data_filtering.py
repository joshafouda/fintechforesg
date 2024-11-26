import pandas as pd

def filter_data(merged_data):
    """
    Pré-filtre la base de données fusionnée pour obtenir une base propre et fiable.

    Args:
        merged_data (pd.DataFrame): DataFrame fusionnée contenant les données utilisateur et KYC.

    Returns:
        pd.DataFrame: DataFrame filtrée selon les critères définis.
    """
    # Filtre 1 : Utilisateurs actifs dans les 90 derniers jours
    filtered_data = merged_data[merged_data['HAS_USED_MOB_MONEY_IN_LAST_90_DAYS'] == 1]

    # Filtre 2 : Limiter les tranches d'âge à faible risque
    filtered_data = filtered_data[(filtered_data['age'] >= 21) & (filtered_data['age'] <= 60)]

    # Filtre 3 : Inclure uniquement les clients entièrement conformes au KYC
    filtered_data = filtered_data[filtered_data['REGISTRATION_STATUS'] == 'Accepted']

    # Réinitialiser les index
    filtered_data = filtered_data.reset_index(drop=True)
    
    return filtered_data

if __name__ == "__main__":
    # Définir les chemins des fichiers
    merged_data_path = "data/processed/merged_data.csv"
    filtered_data_path = "data/processed/filtered_data.csv"

    # Charger les données fusionnées
    print("Chargement des données fusionnées...")
    merged_data = pd.read_csv(merged_data_path)

    # Appliquer le filtrage
    print("Application des filtres sur les données...")
    filtered_data = filter_data(merged_data)

    # Sauvegarder les résultats
    filtered_data.to_csv(filtered_data_path, index=False)
    print(f"Données filtrées sauvegardées dans {filtered_data_path}")