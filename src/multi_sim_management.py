import pandas as pd
import os

def identify_multi_sim_clients(data):
    """
    Identifie les clients ayant plusieurs cartes SIM avec la même pièce d'identité.

    Args:
        data (pd.DataFrame): DataFrame contenant les colonnes 'ID_TYPE', 'ID_NUMBER', et 'SIM_NUMBER'.

    Returns:
        pd.DataFrame: Clients ayant plus d'une carte SIM avec leurs informations.
    """
    multi_sim_clients = (
        data.groupby(['ID_TYPE', 'ID_NUMBER'])['SIM_NUMBER']
        .nunique()
        .reset_index()
        .rename(columns={'SIM_NUMBER': 'SIM_COUNT'})
    )
    return multi_sim_clients[multi_sim_clients['SIM_COUNT'] > 1]


def select_best_profile(group):
    """
    Sélectionne le meilleur profil pour un client ayant plusieurs SIM.

    Args:
        group (pd.DataFrame): Sous-ensemble de données pour un client.

    Returns:
        pd.Series: Ligne représentant le meilleur profil pour le client.
    """
    group = group.copy()
    segment_mapping = {'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Very High': 5}
    group['Segment_Score'] = group['Segment'].map(segment_mapping)
    group['Max_Credit'] = group[['Nano_Loan', 'Advanced_Credit', 'Macro_Loan', 'Cash_Roller_Over']].max(axis=1)
    group = group.sort_values(['Segment_Score', 'Max_Credit'], ascending=[False, False])
    return group.iloc[0]


def manage_multi_sim_clients(data):
    """
    Gère les clients avec plusieurs SIM en conservant uniquement le meilleur profil.

    Args:
        data (pd.DataFrame): DataFrame contenant les colonnes nécessaires pour la gestion des clients.

    Returns:
        pd.DataFrame: DataFrame finale avec une seule ligne par client.
    """
    # Identifier les clients avec plusieurs SIM
    multi_sim_clients = identify_multi_sim_clients(data)

    # Extraire les détails des clients multi-SIM
    multi_sim_details = data.merge(
        multi_sim_clients[['ID_TYPE', 'ID_NUMBER']],
        on=['ID_TYPE', 'ID_NUMBER'],
        how='inner'
    )

    # Appliquer la sélection du meilleur profil
    best_profiles = multi_sim_details.groupby(['ID_TYPE', 'ID_NUMBER']).apply(select_best_profile).reset_index(drop=True)

    # Identifier les clients à SIM unique
    single_sim_clients = data.merge(
        multi_sim_clients[['ID_TYPE', 'ID_NUMBER']],
        on=['ID_TYPE', 'ID_NUMBER'],
        how='left',
        indicator=True
    )
    single_sim_clients = single_sim_clients[single_sim_clients['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Combiner les données pour créer la DataFrame finale
    final_clients = pd.concat([single_sim_clients, best_profiles], ignore_index=True)
    final_clients.drop(columns=['Segment_Score', 'Max_Credit'], inplace=True)

    return final_clients


def validate_final_clients(data):
    """
    Valide que chaque client est unique et associé à une seule SIM.

    Args:
        data (pd.DataFrame): DataFrame finale des clients.

    Returns:
        None
    """
    # Vérifier l'unicité des ID_NUMBER par ID_TYPE
    unique_clients = data.groupby(['ID_TYPE', 'ID_NUMBER']).size()
    non_unique_clients = unique_clients[unique_clients > 1]

    if not non_unique_clients.empty:
        print("Les clients suivants ont plusieurs lignes dans final_clients :")
        print(non_unique_clients)
    else:
        print("Toutes les lignes de final_clients représentent des clients uniques.")

    # Vérifier qu'il n'y a qu'une seule SIM par client
    multiple_sims = data.groupby(['ID_TYPE', 'ID_NUMBER'])['SIM_NUMBER'].nunique()
    non_unique_sims = multiple_sims[multiple_sims > 1]

    if not non_unique_sims.empty:
        print("Les clients suivants sont associés à plusieurs SIMs dans final_clients :")
        print(non_unique_sims)
    else:
        print("Chaque client dans final_clients est associé à une seule SIM.")


if __name__ == "__main__":
    
    # Définir les chemins des fichiers
    base_path = os.getcwd()
    processed_data_path = os.path.join(base_path, "data", "processed")
    cash_allocated_data_path = os.path.join(processed_data_path, "cash_allocated_data.csv")
    final_clients_path = os.path.join(processed_data_path, "final_clients.csv")

    # Charger les données de crédits alloués
    print("Chargement des données avec crédits alloués...")
    cash_allocated_data = pd.read_csv(cash_allocated_data_path)

    # Gérer les clients avec plusieurs SIM
    final_clients = manage_multi_sim_clients(cash_allocated_data)

    # Valider les résultats
    validate_final_clients(final_clients)

    # Sauvegarder les données finales
    print(f"Sauvegarde des clients finaux dans {final_clients_path}...")
    final_clients.to_csv(final_clients_path, index=False)
    print("Gestion des clients multi-SIM terminée avec succès.")
