import pandas as pd
import dask.dataframe as dd
import os

import dask.dataframe as dd

def process_transactions(input_file, output_file):
    """
    Traite les transactions pour calculer les soldes moyens au 15 et au dernier jour du mois précédent.
    
    Args:
        input_file (str): Chemin du fichier CSV contenant les données brutes des transactions.
        output_file (str): Chemin de sauvegarde du fichier résultant.
        
    Returns:
        None: Le fichier est sauvegardé dans le chemin spécifié.
    """
    # Charger les données
    transactions = dd.read_csv(input_file)

    # Conversion de la colonne `transaction_date` en format datetime
    transactions['transaction_date'] = dd.to_datetime(transactions['transaction_date'])

    # Ajouter des colonnes nécessaires
    transactions['day_of_month'] = transactions['transaction_date'].dt.day
    transactions['days_in_month'] = transactions['transaction_date'].dt.days_in_month

    # Créer des DataFrames pour nameOrig et nameDest
    sim_numbers_orig = transactions[['nameOrig', 'transaction_date', 'newbalanceOrig']].rename(
        columns={'nameOrig': 'SIM_NUMBER', 'newbalanceOrig': 'balance'}
    )
    sim_numbers_dest = transactions[['nameDest', 'transaction_date', 'newbalanceDest']].rename(
        columns={'nameDest': 'SIM_NUMBER', 'newbalanceDest': 'balance'}
    )

    # Fusionner les deux DataFrames pour obtenir une vue complète
    transactions_with_sims = dd.concat([sim_numbers_orig, sim_numbers_dest], axis=0)

    # Filtrer uniquement les transactions pour les dates du 15 et du dernier jour du mois
    transactions_with_sims['day_of_month'] = transactions_with_sims['transaction_date'].dt.day
    transactions_with_sims['days_in_month'] = transactions_with_sims['transaction_date'].dt.days_in_month

    relevant_transactions = transactions_with_sims[
        (transactions_with_sims['day_of_month'] == 15) |
        (transactions_with_sims['day_of_month'] == transactions_with_sims['days_in_month'])
    ]

    # Ajouter la colonne DATE_OF_THE_DAY pour l'agrégation
    relevant_transactions['DATE_OF_THE_DAY'] = relevant_transactions['transaction_date']

    # Grouper par SIM_NUMBER et DATE_OF_THE_DAY, puis calculer la moyenne des soldes
    result = relevant_transactions.groupby(['SIM_NUMBER', 'DATE_OF_THE_DAY'])['balance'].mean().reset_index()

    # Sauvegarder les résultats
    result.compute().to_csv(output_file, index=False)


#process_transactions("/raw/real_transactions_with_dates.csv")


def update_transactions(transactions_file, clients_file, output_file):
    """
    Met à jour le fichier de transactions avec les SIM_NUMBER présents dans le fichier clients,
    standardise les dates et calcule les moyennes des soldes.

    Args:
        transactions_file (str): Chemin du fichier CSV des transactions.
        clients_file (str): Chemin du fichier CSV des clients finaux.
        output_file (str): Chemin de sauvegarde du fichier résultant.
        
    Returns:
        None: Le fichier est sauvegardé dans le chemin spécifié.
    """
    # Charger les données existantes
    transactions_previous_month = pd.read_csv(transactions_file)
    final_clients = pd.read_csv(clients_file)

    # Filtrer les transactions en fonction des SIM_NUMBER présents dans final_clients
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

    # Sauvegarder le fichier mis à jour
    transactions_previous_month.to_csv(output_file, index=False)



#update_transactions(
#    transactions_file="processed/transactions_previous_month.csv",
#    clients_file="processed/final_clients.csv"
#)



def calculate_bonus_malus(input_file, final_clients_file, output_file):
    """
    Calcule les bonus/malus des clients à partir des transactions et sauvegarde les résultats dans un fichier.
    
    Args:
        input_file (str): Chemin du fichier CSV contenant les transactions précédentes.
        final_clients_file (str): Chemin du fichier CSV contenant les informations des clients finaux.
        output_file (str): Chemin de sauvegarde du fichier résultant.
        
    Returns:
        None: Le fichier est sauvegardé dans le chemin spécifié.
    """
    # Charger les données
    transactions_previous_month = pd.read_csv(input_file)
    final_clients = pd.read_csv(final_clients_file)

    # Convertir la colonne DATE_OF_THE_DAY en datetime
    transactions_previous_month['DATE_OF_THE_DAY'] = pd.to_datetime(transactions_previous_month['DATE_OF_THE_DAY'])

    # Filtrer les lignes pour le 15 et le dernier jour
    balance_15 = transactions_previous_month[
        transactions_previous_month['DATE_OF_THE_DAY'].dt.day == 15
    ][['SIM_NUMBER', 'balance']].rename(columns={'balance': 'Balance_First'})

    balance_30 = transactions_previous_month[
        transactions_previous_month['DATE_OF_THE_DAY'].dt.day == 30
    ][['SIM_NUMBER', 'balance']].rename(columns={'balance': 'Balance_Second'})

    # Fusionner les balances avec final_clients
    final_clients = final_clients.merge(balance_15, on='SIM_NUMBER', how='left')
    final_clients = final_clients.merge(balance_30, on='SIM_NUMBER', how='left')

    # Calcul des bonus/malus
    def calculate_bonus_malus(row):
        # Déterminer les bornes de crédit selon le type de crédit
        min_loan, max_loan = 0, 0
        if not pd.isna(row.get('Nano_Loan')):
            min_loan, max_loan = 20, 45
        elif not pd.isna(row.get('Macro_Loan')):
            min_loan, max_loan = 25, 250
        elif not pd.isna(row.get('Advanced_Credit')):
            min_loan, max_loan = 100, 500
        elif not pd.isna(row.get('Cash_Roller_Over')):
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
            bonus_malus = max_loan + (max_loan * 10 / 100)  # 10% par défaut pour ajustement
        else:
            repayment_label = "Uncertain"
            bonus_malus = 0

        return pd.Series([repayment_label, bonus_malus], index=['Repayment_Label', 'Bonus_Malus'])

    # Appliquer la fonction pour calculer les bonus/malus
    final_clients[['Repayment_Label', 'Bonus_Malus']] = final_clients.apply(calculate_bonus_malus, axis=1)

    # Sauvegarder les résultats
    final_clients.to_csv(output_file, index=False)



#calculate_bonus_malus(
#    input_file="processed/transactions_previous_month.csv",
#    final_clients_file="processed/final_clients.csv"
#)



def update_loans_with_bonus_malus(input_file, output_file):
    """
    Met à jour les colonnes des prêts avec les bonus/malus calculés et sauvegarde le fichier résultant.

    Args:
        input_file (str): Chemin du fichier CSV contenant les clients avec bonus/malus.
        output_file (str): Chemin de sauvegarde du fichier résultant.

    Returns:
        None: Le fichier est sauvegardé dans le chemin spécifié.
    """
    # Charger les données
    final_clients = pd.read_csv(input_file)

    # Mettre à jour les colonnes des prêts avec les bonus/malus
    for loan_type in ['Nano_Loan', 'Advanced_Credit', 'Macro_Loan', 'Cash_Roller_Over']:
        updated_column = f"{loan_type}_updated"
        final_clients[updated_column] = final_clients[loan_type] + final_clients['Bonus_Malus']

    # Sauvegarder le fichier avec les colonnes mises à jour
    final_clients.to_csv(output_file, index=False)



#update_loans_with_bonus_malus(
#    input_file="processed/final_clients_with_bonus_malus.csv"
#)


# Exécutable pour tester indépendamment
if __name__ == "__main__":
    # Définir les chemins
    base_path = os.getcwd()

    # Chemins des fichiers
    transactions_file = os.path.join(base_path, "data", "raw", "real_transactions_with_dates.csv")
    final_clients_file = os.path.join(base_path, "data", "processed", "final_clients.csv")
    transactions_previous_month_file = os.path.join(base_path, "data", "processed", "transactions_previous_month.csv")
    final_clients_with_bonus_malus_file = os.path.join(base_path, "data", "processed", "final_clients_with_bonus_malus.csv")
    final_clients_with_updated_loans_file = os.path.join(base_path, "data", "processed", "final_clients_with_updated_loans.csv")

    # Étape 1: Créer le DataFrame des transactions pour le mois précédent
    process_transactions(transactions_file, transactions_previous_month_file)

    # Étape 2: Mettre à jour les transactions avec les informations des clients finaux
    update_transactions(
        transactions_previous_month_file,
        final_clients_file,
        transactions_previous_month_file
    )

    # Étape 3: Calculer le bonus/malus pour les clients
    calculate_bonus_malus(
        transactions_previous_month_file, 
        final_clients_file, 
        final_clients_with_bonus_malus_file
    )

    # Étape 4: Mettre à jour les prêts des clients avec le bonus/malus
    update_loans_with_bonus_malus(
        final_clients_with_bonus_malus_file, 
        final_clients_with_updated_loans_file
    )
    
    print("Le calcul du bonus/malus a été effectué avec succès et les fichiers sont mis à jour.")
