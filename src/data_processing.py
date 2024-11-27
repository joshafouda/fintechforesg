import pandas as pd
import datetime

def load_and_merge_data(user_data_path, kyc_data_path):
    """
    Load user data and KYC data, preprocess them, and merge into a single dataframe.

    Args:
        user_data_path (str): Path to the user data CSV file.
        kyc_data_path (str): Path to the KYC data CSV file.

    Returns:
        pd.DataFrame: Merged and preprocessed dataframe.
    """
    # Load the datasets
    user_data_df = pd.read_csv(user_data_path)
    kyc_data_df = pd.read_csv(kyc_data_path)

    # Ensure date columns are properly formatted
    kyc_data_df['BIRTH_DATE'] = pd.to_datetime(kyc_data_df['BIRTH_DATE'], errors='coerce')
    kyc_data_df['ACQUISITION_DATE'] = pd.to_datetime(kyc_data_df['ACQUISITION_DATE'], errors='coerce')

    # Calculate age and tenure for filtering
    current_date = pd.to_datetime(datetime.datetime.today())
    kyc_data_df['age'] = ((current_date - kyc_data_df['BIRTH_DATE']).dt.days / 365.25).astype(int)
    kyc_data_df['tenure_years'] = ((current_date - kyc_data_df['ACQUISITION_DATE']).dt.days / 365.25).astype(int)

    # Merge the datasets
    merged_data = pd.merge(
        user_data_df,
        kyc_data_df,
        left_on='SIM_NUMBER',
        right_on='SIM_NUMBER',
        how='inner'
    )

    return merged_data


# Code exécuté directement si le script est appelé
if __name__ == "__main__":
    # Chemins des fichiers
    user_data_path = "data/raw/simulated_USER_DATA_with_dates.csv"
    kyc_data_path = "data/raw/simulated_KYC_DATA.csv"

    # Appeler la fonction et générer le fichier fusionné
    merged_data = load_and_merge_data(user_data_path, kyc_data_path)
    
    # Sauvegarder les résultats dans processed/
    output_path = "data/processed/merged_data.csv"
    merged_data.to_csv(output_path, index=False)

    print(f"Merged data saved to {output_path}")
