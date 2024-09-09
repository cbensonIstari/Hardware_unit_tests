import requests
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

def get_artifact_ids(extraction_data):
    """
    Function to extract artifact IDs from any section of the extraction data.
    """
    artifacts = []

    # Recursively search for artifact IDs in the extraction data
    def extract_artifacts_from_section(section):
        if isinstance(section, dict):
            if 'id' in section and 'model_id' in section:
                artifacts.append({
                    'model_id': section.get('model_id'),
                    'artifact_id': section.get('id')
                })
            # Recursively search through nested dictionaries
            for key, value in section.items():
                extract_artifacts_from_section(value)
        elif isinstance(section, list):
            # Search through lists
            for item in section:
                extract_artifacts_from_section(item)
    
    # Start searching for artifacts from the output_data section
    extract_artifacts_from_section(extraction_data.get('output_data', {}))

    return artifacts

def get_all_latest_extractions(csv_filepath):
    """
    Function to iterate over each model ID from the CSV and get all artifact IDs.
    """
    # Read the CSV file
    models_df = pd.read_csv(csv_filepath)
    
    # Create a list to store artifact ID results
    artifact_id_results = []

    # Loop through each model ID in the DataFrame
    for index, row in models_df.iterrows():
        model_id = row['id']
        print(f"Fetching latest extraction for model {model_id}...")
        extraction_data = get_latest_extraction(model_id)
        
        if extraction_data:
            artifacts = get_artifact_ids(extraction_data)
            artifact_id_results.extend(artifacts)
    
    # Convert results to a DataFrame and save to CSV
    results_df = pd.DataFrame(artifact_id_results)
    
    # Specify the output path to save the file in Artifacts/artifacts_list.csv
    output_csv_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Artifacts', 'artifacts_list.csv')
    
    # Save the CSV to the Artifacts folder
    results_df.to_csv(output_csv_filepath, index=False)
    print(f"Artifact IDs saved to {output_csv_filepath}")

if __name__ == '__main__':
    get_all_latest_extractions(csv_filepath)
