import requests
import json

def remove_references(data):
    """
    Removes the "Reference" key from the data if it exists.

    Args:
        data (dict): The JSON data to process.

    Returns:
        dict: The processed data without "Reference" key.
    """
    if isinstance(data, dict):
        if "Reference" in data:
            del data["Reference"]
        for key, value in data.items():
            data[key] = remove_references(value)
    elif isinstance(data, list):
        data = [remove_references(item) for item in data]
    return data

def fetch_and_save_pubchem_compound_data(start_id, end_id, output_file):
    """
    Fetches data from PubChem for compound IDs in the specified range and saves to a JSON file.

    Args:
        start_id (int): The starting compound ID.
        end_id (int): The ending compound ID.
        output_file (str): The filename to save the data.
    """
    results = {}

    for compound_id in range(start_id, end_id + 1):
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{compound_id}/JSON/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            processed_data = remove_references(data)
            results[compound_id] = processed_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for compound {compound_id}: {e}")
            results[compound_id] = {"error": str(e)}

    with open(output_file, "w") as json_file:
        json.dump(results, json_file, indent=4)
    print(f"Data saved to {output_file}")

def fetch_and_save_pubchem_substance_data(start_id, end_id, output_file):
    """
    Fetches data from PubChem for substance IDs in the specified range and saves to a JSON file.

    Args:
        start_id (int): The starting substance ID.
        end_id (int): The ending substance ID.
        output_file (str): The filename to save the data.
    """
    results = {}

    for substance_id in range(start_id, end_id + 1):
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance/{substance_id}/JSON/?version=1"
                
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            processed_data = remove_references(data)
            results[substance_id] = processed_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for substance {substance_id}: {e}")
            results[substance_id] = {"error": str(e)}

    with open(output_file, "w") as json_file:
        json.dump(results, json_file, indent=4)
    print(f"Data saved to {output_file}")

fetch_and_save_pubchem_compound_data(1, 5, "pubchem_compound_data.json")
fetch_and_save_pubchem_substance_data(1, 5, "pubchem_substance_data.json")
