import pandas as pd
from src.data_filtering import filter_data

def test_filter_data():
    # Créer un échantillon de données simulées
    data = {
        'SIM_NUMBER': [1, 2, 3, 4],
        'HAS_USED_MOB_MONEY_IN_LAST_90_DAYS': [1, 0, 1, 1],
        'age': [25, 18, 45, 62],
        'REGISTRATION_STATUS': ['Accepted', 'Pending', 'Accepted', 'Accepted']
    }
    merged_data = pd.DataFrame(data)

    # Appliquer la fonction de filtrage
    filtered_data = filter_data(merged_data)

    # Vérifications
    assert len(filtered_data) == 2, "Le filtrage n'a pas renvoyé le bon nombre de lignes"
    assert all(filtered_data['age'].between(21, 60)), "Des âges hors des limites sont présents"
    assert all(filtered_data['HAS_USED_MOB_MONEY_IN_LAST_90_DAYS'] == 1), "Des utilisateurs inactifs sont présents"
    assert all(filtered_data['REGISTRATION_STATUS'] == 'Accepted'), "Des clients non conformes au KYC sont présents"

    print("Tous les tests ont réussi !")

# Exécuter les tests
if __name__ == "__main__":
    test_filter_data()
