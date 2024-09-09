import os
import json

# Define the path to the 'Downloaded' directory
downloaded_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Artifacts', 'Downloaded')

# Define valid units to check against (add or remove as needed)
valid_units = {
    'mm': 'length',
    'in': 'length',
    'deg': 'angle',
    'rad': 'angle'
}

def check_for_unit_errors(data):
    """
    Function to check for unit inconsistencies within a JSON data structure.
    It assumes that 'unit' and 'value' are present in the data and checks if the units are appropriate.
    """
    errors = []
    
    for entry in data:
        name = entry.get('name')
        value = entry.get('value')
        unit = entry.get('unit')

        # Check if the unit is valid
        if unit not in valid_units:
            errors.append(f"Invalid unit found for {name}: {unit}")
            continue
        
        # Example: Let's assume all 'length' values must be in mm.
        if valid_units[unit] == 'length' and unit == 'in':
            errors.append(f"Unit mismatch for {name}: {value}{unit} should be converted to mm.")
    
    return errors

def process_json_file(file_path):
    """
    Function to read and process a JSON file, checking for unit errors.
    """
    with open(file_path, 'r') as json_file:
        try:
            data = json.load(json_file)
            errors = check_for_unit_errors(data)
            if errors:
                print(f"Errors found in {file_path}:")
                for error in errors:
                    print(error)
            else:
                print(f"No errors found in {file_path}.")
        except json.JSONDecodeError:
            print(f"Could not decode JSON in {file_path}")

def scan_directory_for_json_files(directory):
    """
    Function to scan the 'Downloaded' directory and process any JSON files it contains.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                process_json_file(file_path)

if __name__ == '__main__':
    scan_directory_for_json_files(downloaded_path)
