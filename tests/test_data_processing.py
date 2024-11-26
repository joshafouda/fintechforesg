import os
import pandas as pd
from src.data_processing import load_and_merge_data

def test_load_and_merge_data():
    # Définir les chemins des fichiers de test
    user_data_path = "data/raw/simulated_USER_DATA_with_dates.csv"
    kyc_data_path = "data/raw/simulated_KYC_DATA.csv"

    # Exécuter la fonction
    merged_data = load_and_merge_data(user_data_path, kyc_data_path)

    # Vérifications simples
    assert isinstance(merged_data, pd.DataFrame), "Le résultat devrait être un DataFrame"
    assert not merged_data.empty, "Le DataFrame résultant ne devrait pas être vide"
    assert 'SIM_NUMBER' in merged_data.columns, "La colonne 'SIM_NUMBER' devrait être présente dans le DataFrame"
    print("Tous les tests ont réussi !")

# Exécuter les tests
if __name__ == "__main__":
    test_load_and_merge_data()