import requests
import json
import pandas as pd
import os

# Define the auth_token (replace with your actual token)
auth_token = 'CbI_s9Q5P-chle1LMrhgwEwHyKqijM-yj64puTXxshUC9zXhAFUoTtsHN9J-SbP9JKGCv4c'

# Define the base URL for API
base_url = 'https://file-service-eks.dev.istari.app/api/model'

# Path to models.csv file in the main directory
csv_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models.csv')

def get_latest_extraction(model_id):
    """
    Function to get the latest extraction for a given model ID.
    """
    url = f"{base_url}/{model_id}/latest_extraction"
    headers = {'Authorization': f'Bearer {auth_token}'}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        return None
    else:
        print(f"Failed to retrieve extraction for model {model_id}. Status Code: {response.status_code}")
        return None

def get_all_latest_extractions(csv_filepath):
    """
    Function to iterate over each model ID from the CSV and get the latest extraction.
    """
    # Read the CSV file
    models_df = pd.read_csv(csv_filepath)
    
    # Create a list to store extraction results
    extraction_results = []

    # Loop through each model ID in the DataFrame
    for index, row in models_df.iterrows():
        model_id = row['id']
        print(f"Fetching latest extraction for model {model_id}...")
        extraction_data = get_latest_extraction(model_id)
        
        if extraction_data:
            extraction_results.append({
                'model_id': model_id,
                'extraction_id': extraction_data['id'],
                'status': extraction_data['status'],
                'function': extraction_data['function'],
                'created_at': extraction_data['created_at'],
                'updated_at': extraction_data['updated_at'],
                'artifacts': extraction_data.get('output_data', {}).get('output_model', {}).get('output', [])
            })
    
    # Convert results to a DataFrame and save to CSV
    results_df = pd.DataFrame(extraction_results)
  
    # Specify the output path to save the file in Artifacts/artifacts_list.csv
    output_csv_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Artifacts', 'artifacts_list.csv')
  
    results_df.to_csv(output_csv_filepath, index=False)
    print(f"Extraction results saved to {output_csv_filepath}")

if __name__ == '__main__':
    get_all_latest_extractions(csv_filepath)
