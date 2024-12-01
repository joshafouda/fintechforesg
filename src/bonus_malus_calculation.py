import pandas as pd
import dask.dataframe as dd
import os

def preprocess_transactions(transactions_path, output_path):
    """
    Prétraite les données de transactions pour obtenir les soldes moyens du 15 et du dernier jour de chaque mois.

    Args:
        transactions_path (str): Chemin du fichier de transactions brut.
        output_path (str): Chemin du fichier de transactions prétraitées.

    Returns:
        pd.DataFrame: DataFrame contenant les soldes moyens pour le 15 et le dernier jour du mois.
    """
    print("Prétraitement des données de transactions...")
    
    # Charger les transactions
    transactions = dd.read_csv(transactions_path)
    transactions['transaction_date'] = dd.to_datetime(transactions['transaction_date'])

    # Colonnes temporaires
    sim_numbers_orig = transactions[['nameOrig', 'transaction_date', 'newbalanceOrig']].rename(
        columns={'nameOrig': 'SIM_NUMBER', 'newbalanceOrig': 'balance'}
    )
    sim_numbers_dest = transactions[['nameDest', 'transaction_date', 'newbalanceDest']].rename(
        columns={'nameDest': 'SIM_NUMBER', 'newbalanceDest': 'balance'}
    )

    # Fusionner pour obtenir une vue complète
    transactions_with_sims = dd.concat([sim_numbers_orig, sim_numbers_dest], axis=0)

    # Filtrer pour le 15 et le dernier jour du mois
    transactions_with_sims['day_of_month'] = transactions_with_sims['transaction_date'].dt.day
    transactions_with_sims['days_in_month'] = transactions_with_sims['transaction_date'].dt.days_in_month
    
    relevant_transactions = transactions_with_sims[
        (transactions_with_sims['day_of_month'] == 15) |
        (transactions_with_sims['day_of_month'] == transactions_with_sims['days_in_month'])
    ]

    # Ajouter la colonne DATE_OF_THE_DAY pour l'agrégation
    relevant_transactions['DATE_OF_THE_DAY'] = relevant_transactions['transaction_date']

    # Grouper et calculer les soldes moyens
    result = relevant_transactions.groupby(['SIM_NUMBER', 'DATE_OF_THE_DAY'])['balance'].mean().reset_index()
    
    # Sauvegarder les transactions prétraitées
    result.compute().to_csv(output_path, index=False)

    # Charger les données existantes
    transactions_previous_month = pd.read_csv(output_path)
    final_clients = pd.read_csv(os.path.join(os.getcwd(), "data", "processed", "final_clients.csv"))

    # Filtrer transactions_previous_month en fonction des SIM_NUMBER présents dans final_clients
    transactions_previous_month = transactions_previous_month[
        transactions_previous_month['SIM_NUMBER'].isin(final_clients['SIM_NUMBER'])
    ]

    # Convertir DATE_OF_THE_DAY en datetime pour manipuler les dates
    transactions_previous_month['DATE_OF_THE_DAY'] = pd.to_datetime(transactions_previous_month['DATE_OF_THE_DAY'])

    # Ajouter une colonne fictive pour les dates standardisées (2024-11-15 et 2024-11-30)
    transactions_previous_month['Standardized_Date'] = transactions_previous_month['DATE_OF_THE_DAY'].dt.day.map(
        {15: '2024-11-15', 30: '2024-11-30'}
    )

    # Supprimer les valeurs manquantes dans la colonne 'balance'
    transactions_previous_month = transactions_previous_month.dropna(subset=['balance'])

    # Grouper par SIM_NUMBER et Standardized_Date, puis calculer la moyenne
    transactions_previous_month = (
        transactions_previous_month.groupby(['SIM_NUMBER', 'Standardized_Date'], as_index=False)['balance']
        .mean()
    )

    # Renommer la colonne des dates standardisées pour conserver la structure demandée
    transactions_previous_month.rename(columns={'Standardized_Date': 'DATE_OF_THE_DAY'}, inplace=True)

    # Convertir la colonne DATE_OF_THE_DAY en datetime pour uniformité
    transactions_previous_month['DATE_OF_THE_DAY'] = pd.to_datetime(transactions_previous_month['DATE_OF_THE_DAY'])

    # Réinitialiser l'index pour finaliser
    transactions_previous_month.reset_index(drop=True, inplace=True)

    # Sauvegarde
    transactions_previous_month.to_csv(output_path, index=False)

    print(f"Transactions prétraitées sauvegardées dans {output_path}")
    return transactions_previous_month


def calculate_bonus_malus(final_clients, transactions):
    """
    Calcule les bonus/malus et met à jour les montants de crédit.

    Args:
        final_clients (pd.DataFrame): Données des clients finaux.
        transactions (pd.DataFrame): Transactions prétraitées contenant les soldes moyens.

    Returns:
        pd.DataFrame: Données des clients mises à jour avec les colonnes de bonus/malus.
    """
    print("Calcul des bonus/malus...")

    # Extraire les soldes des 15 et 30
    balance_15 = transactions[transactions['transaction_date'] == 15][['SIM_NUMBER', 'balance']].rename(
        columns={'balance': 'Balance_First'}
    )
    balance_30 = transactions[transactions['transaction_date'] == 30][['SIM_NUMBER', 'balance']].rename(
        columns={'balance': 'Balance_Second'}
    )

    # Fusionner les balances avec les données clients
    final_clients = final_clients.merge(balance_15, on='SIM_NUMBER', how='left')
    final_clients = final_clients.merge(balance_30, on='SIM_NUMBER', how='left')

    def calculate_bonus_malus_row(row):
        # Déterminer les bornes de crédit
        min_loan, max_loan = 0, 0
        if not pd.isna(row['Nano_Loan']):
            min_loan, max_loan = 20, 45
        elif not pd.isna(row['Macro_Loan']):
            min_loan, max_loan = 25, 250
        elif not pd.isna(row['Advanced_Credit']):
            min_loan, max_loan = 100, 500
        elif not pd.isna(row['Cash_Roller_Over']):
            min_loan, max_loan = 100, 500

        # Appliquer les règles de bonus/malus
        if row['Balance_First'] <= 0 or row['Balance_Second'] <= 0:
            repayment_label = "Strong ability to borrow"
            bonus_malus = max_loan + (max_loan * 20 / 100)
        elif row['Balance_First'] > 0 and row['Balance_Second'] > 0:
            repayment_label = "Strong repayment capacity"
            bonus_malus = max_loan - (max_loan * 20 / 100)
        elif row['Balance_First'] > 0 and row['Balance_Second'] <= 0:
            repayment_label = "Ability to borrow"
            bonus_malus = max_loan + (max_loan * 20 / 100) / 2
        else:
            repayment_label = "Uncertain"
            bonus_malus = 0

        return pd.Series([repayment_label, bonus_malus], index=['Repayment_Label', 'Bonus_Malus'])

    # Calculer les colonnes de bonus/malus
    final_clients[['Repayment_Label', 'Bonus_Malus']] = final_clients.apply(calculate_bonus_malus_row, axis=1)

    # Mettre à jour les montants de crédit
    for credit_type in ['Nano_Loan', 'Advanced_Credit', 'Macro_Loan', 'Cash_Roller_Over']:
        updated_col = f"{credit_type}_updated"
        final_clients[updated_col] = final_clients[credit_type] + final_clients['Bonus_Malus']

    return final_clients


# Exécutable pour tester indépendamment
if __name__ == "__main__":
    # Définir les chemins
    base_path = os.getcwd()
    transactions_path = os.path.join(base_path, "data", "raw", "real_transactions_with_dates.csv")
    transactions_output = os.path.join(base_path, "data", "processed", "transactions_previous_month.csv")
    final_clients_path = os.path.join(base_path, "data", "processed", "final_clients.csv")
    updated_clients_path = os.path.join(base_path, "data", "processed", "final_clients_with_updated_loans.csv")

    # Prétraitement des transactions
    transactions = preprocess_transactions(transactions_path, transactions_output)

    # Charger les données des clients finaux
    print("Chargement des données clients finaux...")
    final_clients = pd.read_csv(final_clients_path)

    # Calculer les bonus/malus
    final_clients = calculate_bonus_malus(final_clients, transactions)

    # Sauvegarder les données mises à jour
    print(f"Sauvegarde des clients finaux mis à jour dans {updated_clients_path}...")
    final_clients.to_csv(updated_clients_path, index=False)
