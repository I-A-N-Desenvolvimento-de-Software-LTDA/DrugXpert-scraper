import requests
import json

def remove_references(data):
    """Removes the "Reference" key from the data if it exists."""
    if isinstance(data, dict):
        if "Reference" in data:
            del data["Reference"]
        for key, value in data.items():
            data[key] = remove_references(value)
    elif isinstance(data, list):
        data = [remove_references(item) for item in data]
    return data

def process_substance_data(start_id, end_id, output_file, source_type):
    """Process substance data from start to end ID and save final result"""
    # Fetch data
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

    # Transform data
    transformed_data = []
    for substance_id, substance_data in results.items():
        if "Record" in substance_data:
            record = substance_data["Record"]
            molecule_name = record.get("RecordTitle", "Unknown")
            record_number = record.get("RecordNumber", "Unknown")
            record_type = record.get("RecordType", "Unknown")
            
            sections = record.get("Section", [])
            external_id = "Unknown"
            source = "Unknown"
            source_category = []
            deposit_date = "Unknown"
            modify_date = "Unknown"
            available_date = "Unknown"
            status = "Unknown"
            depositor_comments = []
            related_compounds = []
            
            for section in sections:
                if section.get("TOCHeading") == "Identity":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Source":
                            source = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                        elif subsection.get("TOCHeading") == "External ID":
                            external_id = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                        elif subsection.get("TOCHeading") == "Source Category":
                            categories = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [])
                            source_category = [cat.get("String") for cat in categories if cat.get("String")]
                        elif subsection.get("TOCHeading") == "Deposit Date":
                            deposit_date = subsection.get("Information", [{}])[0].get("Value", {}).get("DateISO8601", ["Unknown"])[0]
                        elif subsection.get("TOCHeading") == "Modify Date":
                            modify_date = subsection.get("Information", [{}])[0].get("Value", {}).get("DateISO8601", ["Unknown"])[0]
                        elif subsection.get("TOCHeading") == "Available Date":
                            available_date = subsection.get("Information", [{}])[0].get("Value", {}).get("DateISO8601", ["Unknown"])[0]
                        elif subsection.get("TOCHeading") == "Status":
                            status = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")

                elif section.get("TOCHeading") == "Depositor Comments":
                    comments = section.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [])
                    depositor_comments = [comment.get("String") for comment in comments if comment.get("String")]

                elif section.get("TOCHeading") == "Related Records":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Related Compounds":
                            compounds = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [])
                            related_compounds = [comp.get("String") for comp in compounds if comp.get("String")]

            transformed_item = {
                "type": source_type,
                "place_loc": "pubchem",
                "moleculeName": molecule_name,
                "recordNumber": record_number,
                "recordType": record_type,
                "externalId": external_id,
                "source": source,
                "sourceCategory": source_category,
                "depositDate": deposit_date,
                "modifyDate": modify_date,
                "availableDate": available_date,
                "status": status,
                "depositorComments": depositor_comments,
                "relatedCompounds": related_compounds
            }
            transformed_data.append(transformed_item)

    # Save final result
    with open(output_file, "w") as json_file:
        json.dump(transformed_data, json_file, indent=4)
    print(f"Final substance data saved to {output_file}")

if __name__ == "__main__":
    process_substance_data(1, 5, "final_pubchem_substance_data.json", "substance")
