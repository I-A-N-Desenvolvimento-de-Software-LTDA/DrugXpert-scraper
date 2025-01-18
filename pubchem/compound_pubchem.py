"""
PubChem Compound Data Processor

This module handles the processing of compound data from PubChem's REST API.
It includes functionality for fetching, transforming, and saving compound
chemical information.

Features:
- Fetches compound data from PubChem API
- Removes unnecessary reference metadata
- Extracts relevant chemical information
- Transforms data into standardized format
- Saves final results to JSON

Author: Israel Neto
Date: 2024
"""

import requests
import json

def remove_references(data):
    """
    Removes reference metadata from the PubChem data structure.
    
    Args:
        data (dict/list): Raw PubChem data structure
        
    Returns:
        dict/list: Cleaned data structure without references
    """
    if isinstance(data, dict):
        if "Reference" in data:
            del data["Reference"]
        for key, value in data.items():
            data[key] = remove_references(value)
    elif isinstance(data, list):
        data = [remove_references(item) for item in data]
    return data

def process_compound_data(start_id, end_id, output_file, source_type):
    """
    Processes compound data from PubChem for a range of compound IDs.
    
    Args:
        start_id (int): Starting compound ID
        end_id (int): Ending compound ID
        output_file (str): Path to output JSON file
        source_type (str): Type identifier for the data source
        
    Output fields:
        - type: Data type identifier
        - place_loc: Source location identifier
        - moleculeName: Chemical name
        - recordNumber: PubChem record number
        - smilesStructure: SMILES notation
        - inchiString: InChI string
        - inchiKey: InChI key
        - molecularFormula: Chemical formula
        - molecularWeight: Molecular mass
        - drugBankId: DrugBank identifier
        - categoryUsage: Drug usage category
    """
    # Fetch data
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

    # Transform data
    transformed_data = []
    for compound_id, compound_data in results.items():
        if "Record" in compound_data:
            record = compound_data["Record"]
            molecule_name = record.get("RecordTitle", "Unknown")
            record_number = record.get("RecordNumber", "Unknown")
            
            sections = record.get("Section", [])
            smiles_structure = "Unknown"
            molecular_weight = "Unknown"
            category_usage = "Unknown"
            inchi_string = "Unknown"
            inchi_key = "Unknown"
            molecular_formula = "Unknown"
            drugbank_id = "Unknown"
            
            for section in sections:
                if section.get("TOCHeading") == "Names and Identifiers":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Computed Descriptors":
                            for subsubsection in subsection.get("Section", []):
                                if subsubsection.get("TOCHeading") == "SMILES":
                                    smiles_structure = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                elif subsubsection.get("TOCHeading") == "InChI":
                                    inchi_string = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                elif subsubsection.get("TOCHeading") == "InChIKey":
                                    inchi_key = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")

                        elif subsection.get("TOCHeading") == "Molecular Formula":
                            molecular_formula = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                        
                        elif subsection.get("TOCHeading") == "Other Identifiers":
                            for identifier in subsection.get("Section", []):
                                if identifier.get("TOCHeading") == "DrugBank ID":
                                    drugbank_id = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")

                elif section.get("TOCHeading") == "Chemical and Physical Properties":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Computed Properties":
                            for subsubsection in subsection.get("Section", []):
                                if subsubsection.get("TOCHeading") == "Molecular Weight":
                                    molecular_weight = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                
                elif section.get("TOCHeading") == "Drug and Medication Information":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Drug Indication":
                            info = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                            if info != "Unknown":
                                category_usage = info.split(".")[0]

            transformed_item = {
                "type": source_type,
                "place_loc": "pubchem",
                "moleculeName": molecule_name,
                "recordNumber": record_number,
                "smilesStructure": smiles_structure,
                "inchiString": inchi_string,
                "inchiKey": inchi_key,
                "molecularFormula": molecular_formula,
                "molecularWeight": molecular_weight,
                "drugBankId": drugbank_id,
                "categoryUsage": category_usage
            }
            transformed_data.append(transformed_item)

    # Save final result
    with open(output_file, "w") as json_file:
        json.dump(transformed_data, json_file, indent=4)
    print(f"Final compound data saved to {output_file}")
 
if __name__ == "__main__":
    process_compound_data(1, 100, "final_pubchem_compound_data.json", "compound")
