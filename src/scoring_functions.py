import pandas as pd
import numpy as np

########### Fonction de Scoring du service Mobile Money ##########
def calculate_mobile_money_scores(filtered_data):
    """
    Calcule les scores Mobile Money pour chaque SIM_NUMBER.

    Args:
        filtered_data (pd.DataFrame): Données pré-filtrées contenant les colonnes nécessaires.

    Returns:
        pd.DataFrame: DataFrame avec deux colonnes : 'SIM_NUMBER' et 'Mobile_Money_Score'.
    """
    # Define transaction and subscription columns
    transaction_columns = [
        'MOB_MONEY_REVENUE', 'TOTAL_SPENT_MOB_MONEY_ACCOUNT', 'TOTAL_LOADING_MONEY_IN_MOB_MONEY',
        'TOTAL_CASHOUT_MOB_MONEY_ACCOUNT', 'TOTAL_CASHOUT_MOB_MONEY_FOR_package_PURCHASE',
        'TOTAL_CASHOUT_MOB_MONEY_TRANSFER_MONEY', 'REFILL_mobile_money_ACCOUNT'
    ]
    
    subscription_columns = [
        'NB_VOICE_PACKAGES_SUBS_VIA_MOB_MONEY', 'NB_DATA_package_SUBS_VIA_MOB_MONEY',
        'NB_SMS_package_SUBS_VIA_MOB_MONEY', 'NB_MIXED_package_SUBS_VIA_MOB_MONEY'
    ]
    
    # Calculate percentiles for transaction and subscription columns
    transaction_percentiles = {
        col: np.percentile(filtered_data[col].dropna(), [20, 40, 60, 80]) for col in transaction_columns
    }
    subscription_percentiles = {
        col: np.percentile(filtered_data[col].dropna(), [20, 40, 60, 80]) for col in subscription_columns
    }
    
    # Define scoring function
    def calculate_mobile_money_score(row):
        scores = []

        # Transaction columns scoring
        for col in transaction_columns:
            value = row[col]
            if value < transaction_percentiles[col][0]:
                scores.append(1)
            elif value < transaction_percentiles[col][1]:
                scores.append(2)
            elif value < transaction_percentiles[col][2]:
                scores.append(3)
            elif value < transaction_percentiles[col][3]:
                scores.append(4)
            else:
                scores.append(5)

        # Subscription columns scoring
        for col in subscription_columns:
            value = row[col]
            if value < subscription_percentiles[col][0]:
                scores.append(1)
            elif value < subscription_percentiles[col][1]:
                scores.append(2)
            elif value < subscription_percentiles[col][2]:
                scores.append(3)
            elif value < subscription_percentiles[col][3]:
                scores.append(4)
            else:
                scores.append(5)

        # Average the scores and round to nearest integer for final score
        final_score = int(round(np.mean(scores)))
        return final_score
    
    # Apply the scoring function to the dataframe
    filtered_data['Mobile_Money_Score'] = filtered_data.apply(calculate_mobile_money_score, axis=1)
    
    # Return the result as a new dataframe 
    return filtered_data


########### Fonction de Scoring du service Data ##########
def calculate_data_service_scores(filtered_data):
    """
    Calcule les scores du service Data pour chaque SIM_NUMBER.

    Args:
        filtered_data (pd.DataFrame): Données pré-filtrées contenant les colonnes nécessaires.

    Returns:
        pd.DataFrame: DataFrame avec deux colonnes : 'SIM_NUMBER' et 'Data_Service_Score'.
    """
    # Define data usage, subscription, and activity columns
    data_usage_columns = ['PAID_DATA_VOLUME', 'DATA_REVENUE', 'FREE_DATA_VOLUME']
    data_subscription_columns = [
        'NB_DATA_PACKAGES_SUBSCRIPTIONS', 'NB_DATA_package_SUBS_VIA_POS',
        'NB_DATA_package_SUBS_VIA_MAIN_ACCOUNT'
    ]
    data_activity_column = ['IS_DATA_RGS90']

    # Calculate percentiles for usage and subscription columns
    data_usage_percentiles = {
        col: np.percentile(filtered_data[col].dropna(), [20, 40, 60, 80]) for col in data_usage_columns
    }
    data_subscription_percentiles = {
        col: np.percentile(filtered_data[col].dropna(), [20, 40, 60, 80]) for col in data_subscription_columns
    }

    # Define scoring function for Data service
    def calculate_data_service_score(row):
        scores = []

        # Data usage columns scoring based on percentiles
        for col in data_usage_columns:
            value = row[col]
            if value < data_usage_percentiles[col][0]:
                scores.append(1)
            elif value < data_usage_percentiles[col][1]:
                scores.append(2)
            elif value < data_usage_percentiles[col][2]:
                scores.append(3)
            elif value < data_usage_percentiles[col][3]:
                scores.append(4)
            else:
                scores.append(5)

        # Data subscription columns scoring based on percentiles
        for col in data_subscription_columns:
            value = row[col]
            if value < data_subscription_percentiles[col][0]:
                scores.append(1)
            elif value < data_subscription_percentiles[col][1]:
                scores.append(2)
            elif value < data_subscription_percentiles[col][2]:
                scores.append(3)
            elif value < data_subscription_percentiles[col][3]:
                scores.append(4)
            else:
                scores.append(5)

        # Activity column scoring
        for col in data_activity_column:
            if row[col] == 1:
                scores.append(5)  # High score for recent activity
            else:
                scores.append(1)  # Low score if no recent activity

        # Average the scores and round to nearest integer for final score
        final_score = int(round(np.mean(scores)))
        return final_score

    # Apply the scoring function to the dataframe
    filtered_data['Data_Service_Score'] = filtered_data.apply(calculate_data_service_score, axis=1)

    # Return the result as a new dataframe 
    return filtered_data


########### Fonction de scoring du service Voice ##########
def calculate_voice_service_scores(filtered_data):
    """
    Calcule les scores Voice Service pour chaque SIM_NUMBER.

    Args:
        filtered_data (pd.DataFrame): Données pré-filtrées contenant les colonnes nécessaires.

    Returns:
        pd.DataFrame: DataFrame avec deux colonnes : 'SIM_NUMBER' et 'Voice_Service_Score'.
    """
    # Define voice usage and subscription columns
    voice_usage_columns = [
        'PAID_VOICE_TRAFFIC', 'VOICE_REVENUE', 'FREE_VOICE_TRAFFIC', 'VOICE_TRAFFIC_ONNET',
        'VOICE_TRAFFIC_OFFNET', 'VOICE_OUTGOING_TRAFFIC_INTERNATIONAL', 'VOICE_INCOMING_TRAFFIC_INTERNATIONAL',
        'VOICE_OUTGOING_TRAFFIC_ONNET', 'VOICE_INCOMING_TRAFFIC_ONNET',
        'VOICE_OUTGOING_TRAFFIC_OFFNET', 'VOICE_INCOMING_TRAFFIC_OFFNET',
        'NB_CALLS_EMITTED_ONNET', 'NB_CALLS_RECEIVED_ONNET', 'NB_CALLS_EMITTED_OFFNET',
        'NB_CALLS_RECEIVED_OFFNET', 'VOICE_PACKAGES_REVENUE'
    ]
    voice_subscription_columns = [
        'NB_VOICE_PACKAGES_SUBSCRIPTIONS', 'NB_VOICE_PACKAGES_SUBS_VIA_POS',
        'NB_VOICE_PACKAGES_SUBS_VIA_MAIN_ACCOUNT'
    ]

    # Calculate percentiles for voice usage and subscription columns
    voice_usage_percentiles = {
        col: np.percentile(filtered_data[col].dropna(), [20, 40, 60, 80]) for col in voice_usage_columns
    }
    voice_subscription_percentiles = {
        col: np.percentile(filtered_data[col].dropna(), [20, 40, 60, 80]) for col in voice_subscription_columns
    }

    # Define scoring function for Voice Service
    def calculate_voice_service_score(row):
        scores = []

        # Voice usage columns scoring
        for col in voice_usage_columns:
            value = row[col]
            if value < voice_usage_percentiles[col][0]:
                scores.append(1)
            elif value < voice_usage_percentiles[col][1]:
                scores.append(2)
            elif value < voice_usage_percentiles[col][2]:
                scores.append(3)
            elif value < voice_usage_percentiles[col][3]:
                scores.append(4)
            else:
                scores.append(5)

        # Voice subscription columns scoring
        for col in voice_subscription_columns:
            value = row[col]
            if value < voice_subscription_percentiles[col][0]:
                scores.append(1)
            elif value < voice_subscription_percentiles[col][1]:
                scores.append(2)
            elif value < voice_subscription_percentiles[col][2]:
                scores.append(3)
            elif value < voice_subscription_percentiles[col][3]:
                scores.append(4)
            else:
                scores.append(5)

        # Average the scores and round to the nearest integer
        final_score = int(round(np.mean(scores)))
        return final_score

    # Apply the scoring function to the dataframe
    filtered_data['Voice_Service_Score'] = filtered_data.apply(calculate_voice_service_score, axis=1)

    # Return the result as a new dataframe 
    return filtered_data



########## Fonction de scoring du service SMS ###########
def calculate_sms_service_scores(filtered_data):
    """
    Calcule les scores SMS Service pour chaque SIM_NUMBER.

    Args:
        filtered_data (pd.DataFrame): Données pré-filtrées contenant les colonnes nécessaires.

    Returns:
        pd.DataFrame: DataFrame avec deux colonnes : 'SIM_NUMBER' et 'SMS_Service_Score'.
    """
    # Define SMS usage and subscription columns
    sms_usage_columns = [
        'SMS_REVENUE', 'NB_SMS_SENT_ONNET', 'NB_SMS_SENT_OFFNET', 'NB_SMS_RECEIVED_ONNET',
        'NB_SMS_RECEIVED_OFFNET', 'NB_SMS_SENT_INTERNATIONAL', 'NB_SMS_RECEIVED_INTERNATIONAL',
        'SMS_PACKAGE_REVENUE'
    ]
    sms_subscription_columns = [
        'NB_SMS_PACKAGES_SUBSCRIPTIONS', 'NB_SMS_package_SUBS_VIA_POS',
        'NB_SMS_package_SUBS_VIA_MAIN_ACCOUNT'
    ]

    # Calculate percentiles for SMS usage and subscription columns
    sms_usage_percentiles = {
        col: np.percentile(filtered_data[col].dropna(), [20, 40, 60, 80]) for col in sms_usage_columns
    }
    sms_subscription_percentiles = {
        col: np.percentile(filtered_data[col].dropna(), [20, 40, 60, 80]) for col in sms_subscription_columns
    }

    # Define scoring function for SMS Service
    def calculate_sms_service_score(row):
        scores = []

        # SMS usage columns scoring
        for col in sms_usage_columns:
            value = row[col]
            if value < sms_usage_percentiles[col][0]:
                scores.append(1)
            elif value < sms_usage_percentiles[col][1]:
                scores.append(2)
            elif value < sms_usage_percentiles[col][2]:
                scores.append(3)
            elif value < sms_usage_percentiles[col][3]:
                scores.append(4)
            else:
                scores.append(5)

        # SMS subscription columns scoring
        for col in sms_subscription_columns:
            value = row[col]
            if value < sms_subscription_percentiles[col][0]:
                scores.append(1)
            elif value < sms_subscription_percentiles[col][1]:
                scores.append(2)
            elif value < sms_subscription_percentiles[col][2]:
                scores.append(3)
            elif value < sms_subscription_percentiles[col][3]:
                scores.append(4)
            else:
                scores.append(5)

        # Average the scores and round to the nearest integer
        final_score = int(round(np.mean(scores)))
        return final_score

    # Apply the scoring function to the dataframe
    filtered_data['SMS_Service_Score'] = filtered_data.apply(calculate_sms_service_score, axis=1)

    # Return the result as a new dataframe
    return filtered_data


########## Fonction de scoring du service Digital ##########
def calculate_digital_service_scores(filtered_data):
    """
    Calcule les scores Digital Service pour chaque SIM_NUMBER.

    Args:
        filtered_data (pd.DataFrame): Données pré-filtrées contenant les colonnes nécessaires.

    Returns:
        pd.DataFrame: DataFrame avec deux colonnes : 'SIM_NUMBER' et 'Digital_Service_Score'.
    """
    # Calculate percentiles for DIGITAL_REVENUE
    digital_revenue_percentiles = np.percentile(
        filtered_data['DIGITAL_REVENUE'].dropna(), [20, 40, 60, 80]
    )

    # Define scoring function for Digital Service
    def calculate_digital_service_score(row):
        scores = []

        # Digital revenue scoring based on percentile thresholds
        digital_revenue = row['DIGITAL_REVENUE']
        if digital_revenue < digital_revenue_percentiles[0]:
            scores.append(1)
        elif digital_revenue < digital_revenue_percentiles[1]:
            scores.append(2)
        elif digital_revenue < digital_revenue_percentiles[2]:
            scores.append(3)
        elif digital_revenue < digital_revenue_percentiles[3]:
            scores.append(4)
        else:
            scores.append(5)

        # Calculate the average score for Digital Service
        final_score = int(round(np.mean(scores)))
        return final_score

    # Apply the scoring function to the dataframe
    filtered_data['Digital_Service_Score'] = filtered_data.apply(
        calculate_digital_service_score, axis=1
    )

    # Return the result as a new dataframe 
    return filtered_data


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
        filtered_data['Mobile_Money_Score'].astype(int).astype(str) +
        filtered_data['Data_Service_Score'].astype(int).astype(str) +
        filtered_data['Voice_Service_Score'].astype(int).astype(str) +
        filtered_data['SMS_Service_Score'].astype(int).astype(str) +
        filtered_data['Digital_Service_Score'].astype(int).astype(str)
    )
    return filtered_data


