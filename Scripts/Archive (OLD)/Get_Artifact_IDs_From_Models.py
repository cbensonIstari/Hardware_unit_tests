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

def extract_artifacts(extraction_data):
    """
    Function to extract all artifacts from the extraction data.
    """
    artifacts = []
    
    # Extract the main output artifact if present
    if 'output_model' in extraction_data.get('output_data', {}):
        output = extraction_data['output_data']['output_model'].get('output', {})
        artifacts.append(output)
    
    # Extract diagrams if present
    if 'diagrams' in extraction_data.get('output_data', {}):
        diagrams = extraction_data['output_data']['diagrams'].get('output', [])
        artifacts.extend(diagrams)
    
    # Extract blocks if present
    if 'blocks' in extraction_data.get('output_data', {}):
        blocks = extraction_data['output_data']['blocks'].get('output', {})
        artifacts.append(blocks)
    
    # Extract requirements if present
    if 'requirements' in extraction_data.get('output_data', {}):
        requirements = extraction_data['output_data']['requirements'].get('output', {})
        artifacts.append(requirements)

    return artifacts

def get_all_latest_extractions(csv_filepath):
    """
    Function to iterate over each model ID from the CSV and get all extracted artifacts.
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
            artifacts = extract_artifacts(extraction_data)
            
            for artifact in artifacts:
                extraction_results.append({
                    'model_id': model_id,
                    'artifact_id': artifact.get('id'),
                    'artifact_name': artifact.get('name'),
                    'artifact_type': artifact.get('artifact_type'),
                    'file_type': artifact.get('file_type'),
                    'created_at': artifact.get('created_at'),
                    'updated_at': artifact.get('updated_at')
                })
    
    # Convert results to a DataFrame and save to CSV
    results_df = pd.DataFrame(extraction_results)
    
    # Specify the output path to save the file in Artifacts/artifacts_list.csv
    output_csv_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Artifacts', 'artifacts_list.csv')
    
    # Save the CSV to the Artifacts folder
    results_df.to_csv(output_csv_filepath, index=False)
    print(f"Extraction results saved to {output_csv_filepath}")

if __name__ == '__main__':
    get_all_latest_extractions(csv_filepath)
