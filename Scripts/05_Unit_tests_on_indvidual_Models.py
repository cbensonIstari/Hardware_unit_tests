import os
import json
import pandas as pd

# Define valid units and their corresponding types (for checking)
valid_units = {
    'mm': 'length',
    'cm': 'length',
    'm': 'length',
    'deg': 'angle',
    'rad': 'angle',
    'in': 'length',
    'ft': 'length',
    'kg': 'mass',
    'g': 'mass',
    'N': 'force',
    'Pa': 'pressure',
    'MPa': 'pressure',
    # Add more units as required
}

# Define the path to the log output file
log_output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Logs', 'unit_test_log.md')

def check_for_unit_errors(data):
    """
    Function to check for unit inconsistencies within a JSON data structure.
    It assumes that 'unit' and 'value' are present in the data and checks if the units are appropriate.
    """
    errors = []
    
    # Check if the data is a list or dictionary
    if isinstance(data, list):
        for entry in data:
            # Ensure each entry is a dictionary
            if isinstance(entry, dict):
                name = entry.get('name')
                value = entry.get('value')
                unit = entry.get('unit')

                # Check if the 'unit' field is missing or null
                if not unit:
                    errors.append(f"**Missing unit** for `{name}` with value `{value}`.")
                    continue

                # Check if the unit is valid
                if unit not in valid_units:
                    errors.append(f"**Invalid unit** found for `{name}`: `{unit}`.")
                    continue

                # Example: Let's assume all 'length' values must be in mm.
                if valid_units[unit] == 'length' and unit == 'in':
                    errors.append(f"**Unit mismatch** for `{name}`: `{value}{unit}` should be converted to `mm`.")
            else:
                errors.append(f"**Invalid data structure**: Expected a dictionary but got {type(entry)}.")
    else:
        errors.append(f"**Invalid data structure**: Expected a list but got {type(data)}.")
    
    return errors

def process_json_file(file_path):
    """
    Function to process a JSON file and return any unit errors.
    """
    with open(file_path, 'r') as json_file:
        try:
            data = json.load(json_file)
            errors = check_for_unit_errors(data)
        except json.JSONDecodeError as e:
            return file_path, [f"**JSON Decode Error**: {str(e)}"]
        except Exception as e:
            return file_path, [f"**Error**: {str(e)}"]
    
    return file_path, errors

def scan_directory_for_json_files(directory_path):
    """
    Function to scan a directory for JSON files and process them for unit errors.
    """
    results = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                file_path, errors = process_json_file(file_path)
                results.append((file_path, errors))
    
    return results

def write_log_file(results, log_output_path):
    """
    Function to write the results of the unit tests to a markdown log file.
    """
    with open(log_output_path, 'w') as log_file:
        log_file.write("# Unit Test Log\n\n")
        
        for file_path, errors in results:
            log_file.write(f"## File: {file_path}\n")
            if errors:
                log_file.write(f"**Errors Found:**\n")
                for error in errors:
                    log_file.write(f"- {error}\n")
            else:
                log_file.write(f"No errors found.\n")
            log_file.write("\n")
    
    print(f"Log file written to {log_output_path}")

if __name__ == '__main__':
    # Define the path to the 'Downloaded' directory
    downloaded_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Artifacts', 'Downloaded')
    
    # Scan the directory for JSON files and process them
    results = scan_directory_for_json_files(downloaded_path)
    
    # Write the results to a log file
    write_log_file(results, log_output_path)
