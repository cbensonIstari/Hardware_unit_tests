import requests
import json
import pandas as pd

def get_models(base_url, query_params):
    # Fetch the auth token from environment variables
    auth_token = 'CbI_s9Q5P-chle1LMrhgwEwHyKqijM-yj64puTXxshUC9zXhAFUoTtsHN9J-SbP9JKGCv4c'

    # Headers with the JWT token for authorization
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }

    # Make the GET request with the provided query parameters
    response = requests.get(base_url, headers=headers, params=query_params)
    print("Status Code:", response.status_code)

    # Process the response
    if response.status_code == 200:
        response_data = response.json()
        print("Models Retrieved Successfully")
        # Expand the data for the CSV format
        expanded_data = []
        for item in response_data['items']:
            for grant in item['user_grants']:
                expanded_data.append({
                    'name': item['name'],
                    'id': item['id'],
                    'creator_id': item['creator_id'],
                    'processing_status': item['processing_status'],
                    'model_type': item['model_type'],
                    'creator_name': item['creator']['name'],
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at'],
                    'grant': grant['grant'],
                    'grant_user_name': grant['user']['name'],
                    'grant_user_given_name': grant['user']['given_name'],
                    'grant_user_family_name': grant['user']['family_name']
                })

        # Convert expanded data to DataFrame and save to CSV
        df_expanded = pd.DataFrame(expanded_data)
        csv_filename = "models.csv"
        df_expanded.to_csv(csv_filename, index=False)
        print(f"CSV saved as {csv_filename}")

    else:
        print("Failed to retrieve models:", response.text)


if __name__ == '__main__':
    # API details
    base_url = 'https://file-service-eks.dev.istari.app/api/model/'

    # Query parameters as a dictionary
    query_params = {
        'name__like': 'Digital_One',  # Filter by name if necessary
        'page': 1,
        'size': 50
    }

    # Get models and output to CSV
    get_models(base_url, query_params)
