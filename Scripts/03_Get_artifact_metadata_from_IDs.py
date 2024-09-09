import csv
import requests
import os
import json

# File paths
artifacts_list_path = './Artifacts/artifacts_list.csv'
output_path = './Artifacts/artifact_metadata.csv'

# Function to retrieve artifact metadata by model_id and artifact_id
def get_artifact_metadata(model_id, artifact_id, token):
    url = f'https://file-service-eks.dev.istari.app/api/model/{model_id}/artifact/{artifact_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve metadata for artifact {artifact_id}. Status code: {response.status_code}")
        return None

# Read the artifact list
with open(artifacts_list_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    artifact_rows = list(csv_reader)

# Placeholder for metadata results
artifact_metadata = []

# Replace this with your actual API token
api_token = "CbI_s9Q5P-chle1LMrhgwEwHyKqijM-yj64puTXxshUC9zXhAFUoTtsHN9J-SbP9JKGCv4c"

# Retrieve metadata for each artifact and append to list
for row in artifact_rows:
    model_id = row['model_id']
    artifact_id = row['artifact_id']
    
    metadata = get_artifact_metadata(model_id, artifact_id, api_token)
    
    if metadata:
        artifact_metadata.append({
            'model_id': model_id,
            'artifact_id': artifact_id,
            'artifact_name': metadata['name'],
            'artifact_extension': metadata['artifact_extension'],
            'file_size_bytes': metadata.get('file_size_bytes', 'N/A'),
            'artifact_status': metadata['artifact_status'],
            'created_at': metadata['created_at'],
            'updated_at': metadata['updated_at'],
            'signed_download_url': metadata.get('signed_download_url', 'N/A')
        })

# Write the metadata to a new CSV file
with open(output_path, mode='w', newline='') as file:
    fieldnames = ['model_id', 'artifact_id', 'artifact_name', 'artifact_extension', 'file_size_bytes', 'artifact_status', 'created_at', 'updated_at', 'signed_download_url']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(artifact_metadata)

print(f"Artifact metadata saved to {output_path}")
