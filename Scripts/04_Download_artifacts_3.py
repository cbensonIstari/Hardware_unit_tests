import requests
import os
import pandas as pd
import time

# Define the auth_token (replace with your actual token)
auth_token = 'CbI_s9Q5P-chle1LMrhgwEwHyKqijM-yj64puTXxshUC9zXhAFUoTtsHN9J-SbP9JKGCv4c'

# Define the base URL for Istari API
base_url = 'https://file-service-eks.dev.istari.app/api/model'

# List of file extensions that are natively viewable by GitHub
viewable_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.json', '.txt', '.md', '.xml', '.html', '.csv', '.yaml', '.yml', '.rst']

# Path to artifact_metadata.csv and models.csv
metadata_csv_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Artifacts', 'artifact_metadata.csv')
models_csv_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models.csv')

# Define the main output folder for downloaded artifacts
artifacts_output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Artifacts', 'Downloaded')

# Create the output folder if it doesn't exist
if not os.path.exists(artifacts_output_folder):
    os.makedirs(artifacts_output_folder)

def load_model_names(models_csv_filepath):
    """
    Function to load model names from models.csv and return a dictionary mapping model_id to model_name.
    """
    models_df = pd.read_csv(models_csv_filepath)
    model_name_map = {row['id']: row['name'] for _, row in models_df.iterrows()}
    return model_name_map

def get_artifact_metadata(model_id, artifact_id):
    """
    Function to get artifact metadata from Istari API by model_id and artifact_id.
    """
    url = f"{base_url}/{model_id}/artifact/{artifact_id}"
    headers = {'Authorization': f'Bearer {auth_token}'}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve artifact {artifact_id} for model {model_id}. Status Code: {response.status_code}")
        return None

def download_artifact(artifact_name, download_url, file_extension, model_name):
    """
    Function to download an artifact and save it to the specified folder.
    """
    # Create a folder for the model if it doesn't exist
    model_folder_path = os.path.join(artifacts_output_folder, model_name)
    if not os.path.exists(model_folder_path):
        os.makedirs(model_folder_path)

    # Download the artifact
    response = requests.get(download_url)
    
    if response.status_code == 200:
        file_path = os.path.join(model_folder_path, f"{artifact_name}{file_extension}")
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {artifact_name}{file_extension} into {model_name}")
    else:
        print(f"Failed to download {artifact_name}. Status Code: {response.status_code}")
        return response.status_code

def process_artifacts():
    """
    Function to process each artifact in artifact_metadata.csv.
    """
    # Load the model names from models.csv
    model_name_map = load_model_names(models_csv_filepath)

    # Read the artifact metadata CSV file
    metadata_df = pd.read_csv(metadata_csv_filepath)

    # Loop through each row in the CSV
    for index, row in metadata_df.iterrows():
        model_id = row['model_id']
        artifact_id = row['artifact_id']
        artifact_name = row['artifact_name']
        file_extension = f".{row['artifact_extension']}"  # Get the file extension
        download_url = row.get('signed_download_url')

        # Get the model name based on the model_id
        model_name = model_name_map.get(model_id, f"Model_{model_id}")  # Fallback if no name found

        # Check if the file extension is in the list of GitHub-viewable formats
        if file_extension in viewable_extensions:
            if download_url and 'null' not in download_url:  # Ensure the download URL exists
                status_code = download_artifact(artifact_name, download_url, file_extension, model_name)

                # Handle 403 error by refreshing the download URL
                if status_code == 403:
                    print(f"Download link for {artifact_name} is expired or forbidden. Fetching metadata again...")
                    artifact_metadata = get_artifact_metadata(model_id, artifact_id)
                    if artifact_metadata:
                        # Extract the new download URL and retry download
                        new_download_url = artifact_metadata.get('signed_download_url')
                        if new_download_url:
                            download_artifact(artifact_name, new_download_url, file_extension, model_name)
                        else:
                            print(f"New download URL for {artifact_name} not found.")
                    else:
                        print(f"Could not retrieve metadata for {artifact_name}. Skipping.")
            else:
                print(f"Download link for {artifact_name} is missing or invalid.")
        else:
            print(f"Skipping {artifact_name} due to unsupported file format: {file_extension}")
        
        # Delay between requests to avoid overwhelming the server
        time.sleep(1)

if __name__ == '__main__':
    process_artifacts()
