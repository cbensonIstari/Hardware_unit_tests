import requests
import json

def get_latest_extraction(model_id):
    # Define the auth_token
    auth_token = 'CbI_s9Q5P-chle1LMrhgwEwHyKqijM-yj64puTXxshUC9zXhAFUoTtsHN9J-SbP9JKGCv4c'

    base_url = 'https://file-service-eks.dev.istari.app/api/model'

    # Construct the full URL to access the latest extraction endpoint
    url = f"{base_url}/{model_id}/latest_extraction"

    # Set up the headers with the JWT for authorization
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }

    # Make the GET request
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")

    # Handle the response based on the status code
    if response.status_code == 200:
        print("Latest extraction task retrieved successfully:")
        print(json.dumps(response.json(), indent=4))
    elif response.status_code in [202, 204, 400, 403, 404, 409, 422]:
        # Handle different cases based on the status code
        print("Response:", response.status_code)
        if response.status_code == 204:
            print("No extraction has been done on this model.")
        elif response.text:
            print(response.text)
        else:
            print("No content or error occurred.")
    else:
        print("Failed to retrieve latest extraction:", response.text)

if __name__ == '__main__':
    # API and Authentication details

    # Model ID for which the version history is required
    model_id = '30566b0c-4de2-4825-ac28-572bdf4ef39a'

    # Call the function to get the latest extraction
    get_latest_extraction(model_id)