import os
import json
from datetime import datetime

# Define the path to the log output file
log_output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Logs', 'integration_test_log.md')

# Placeholder Model and Artifact IDs for generating the Istari link (adjust as needed)
model_id = '30566b0c-4de2-4825-ac28-572bdf4ef39a'
artifact_id = 'bf728430-f25b-4912-943d-c71fce0d2f1c'

def load_json(file_path):
    """
    Function to load a JSON file from the given file path.
    Tries to handle encoding issues gracefully by attempting multiple encodings.
    Returns the loaded data and an error (if any).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data, None  # Return data and no error
    except UnicodeDecodeError:
        # Try a fallback encoding (ISO-8859-1 or Latin-1, common alternative)
        try:
            with open(file_path, 'r', encoding='ISO-8859-1') as json_file:
                data = json.load(json_file)
                return data, None
        except Exception as e:
            return None, f"**Error**: Unable to decode {file_path} with ISO-8859-1. {str(e)}"
    except json.JSONDecodeError as e:
        return None, f"**JSON Decode Error**: {str(e)}"
    except Exception as e:
        return None, f"**Error**: {str(e)}"

def extract_catia_wing_length(catia_data):
    """
    Function to extract the 'WING_LENGTH' value from CATIA parameters.json.
    """
    for entry in catia_data:
        if entry.get('name') == 'WING_LENGTH':
            return float(entry.get('value')), None
    return None, "WING_LENGTH not found in CATIA data"

def extract_cameo_wingspan(cameo_data):
    """
    Function to extract the 'Wingspan' value from the Cameo model (Block Wings).
    """
    for block in cameo_data:
        if block.get('name') == 'Block Wings':
            owned_attributes = block.get('owned_attributes', {})
            wingspan = owned_attributes.get('Wingspan')
            if wingspan:
                return float(wingspan), None
    return None, "Wingspan not found in Cameo data"

def compare_values(catia_value, cameo_value):
    """
    Function to compare the values from CATIA and Cameo models.
    """
    if catia_value == cameo_value:
        return True, None
    else:
        return False, f"Values do not match: CATIA WING_LENGTH is {catia_value} and Cameo Wingspan is {cameo_value}"

def run_integration_test(catia_file_path, cameo_file_path):
    """
    Function to run the integration test comparing WING_LENGTH and Wingspan.
    """
    # Load the CATIA parameters.json
    catia_data, error = load_json(catia_file_path)
    if error:
        return False, error
    
    # Load the Cameo cameo_json_output.json
    cameo_data, error = load_json(cameo_file_path)
    if error:
        return False, error
    
    # Extract WING_LENGTH from CATIA data
    catia_wing_length, error = extract_catia_wing_length(catia_data)
    if error:
        return False, error
    
    # Extract Wingspan from Cameo data
    cameo_wingspan, error = extract_cameo_wingspan(cameo_data)
    if error:
        return False, error
    
    # Compare the two values
    are_aligned, error = compare_values(catia_wing_length, cameo_wingspan)
    return are_aligned, error

def write_log_file(result, log_output_path, model_id, artifact_id, error=None):
    """
    Function to write the results of the integration test to a markdown log file.
    Adds timestamps, Istari links, and error messages in case of test failure.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    istari_link = f"https://dev.istari.app/file/{model_id}/artifact/{artifact_id}"

    with open(log_output_path, 'a') as log_file:
        log_file.write("# Integration Test Log\n\n")
        log_file.write(f"**Test Run Time**: {timestamp}\n\n")
        log_file.write(f"**Istari Artifact Link**: [{istari_link}]({istari_link})\n\n")
        log_file.write("## Test: Compare WING_LENGTH and Wingspan\n\n")
        
        if result and not error:
            log_file.write("<span style='color: green;'>**Test Passed**: The WING_LENGTH from CATIA matches the Wingspan from Cameo.</span>\n")
        else:
            log_file.write("<span style='color: red;'>**Test Failed**: The WING_LENGTH from CATIA does not match the Wingspan from Cameo.</span>\n")
            if error:
                log_file.write(f"<span style='color: red;'>**Error Details**: {error}</span>\n")
        log_file.write("\n")

    print(f"Log file written to {log_output_path}")

if __name__ == '__main__':
    # Define the paths to the CATIA parameters.json and Cameo cameo_json_output.json
    catia_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Artifacts', 'Downloaded', 'Digital_One_CATIA_v5_CAD_IstariOne.zip', 'parameters.json')
    cameo_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Artifacts', 'Downloaded', 'Digital_One_CAMEO_IstariONE.mdzip', 'cameo_json_output.json')
    
    # Run the integration test
    result, error = run_integration_test(catia_file_path, cameo_file_path)
    
    # Write the results to the log file with detailed formatting
    write_log_file(result, log_output_path, model_id, artifact_id, error)
