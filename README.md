# PubChem Data Scraper

## Overview
This project contains scripts to fetch and process compound and substance data from PubChem's REST API. It extracts chemical information, transforms it into a standardized format, and saves it as JSON files.

## Project Structure
```
pubchem/
├── main_pubchem.py        # Main orchestrator script
├── compound_pubchem.py    # Compound data processing
└── substance_pubchem.py   # Substance data processing
```

## Features
- Fetches compound and substance data from PubChem
- Removes reference metadata
- Transforms data into a standardized format
- Combines compound and substance data processing
- Outputs final JSON files with complete information

## Requirements
- Python 3.7+
- requests library

## Installation
```bash
pip install requests
```

## Usage

### Running the Complete Pipeline
To process both compound and substance data:
```bash
python main_pubchem.py
```

### Running Individual Components
To process only compounds:
```bash
python compound_pubchem.py
```

To process only substances:
```bash
python substance_pubchem.py
```

## Output Files
- `final_pubchem_compound_data.json`: Processed compound data
- `final_pubchem_substance_data.json`: Processed substance data

## Data Structure

### Compound Data Format
```json
{
    "type": "compound",
    "place_loc": "pubchem",
    "moleculeName": "string",
    "recordNumber": "number",
    "smilesStructure": "string",
    "inchiString": "string",
    "inchiKey": "string",
    "molecularFormula": "string",
    "molecularWeight": "string",
    "drugBankId": "string",
    "categoryUsage": "string"
}
```

### Substance Data Format
```json
{
    "type": "substance",
    "place_loc": "pubchem",
    "moleculeName": "string",
    "recordNumber": "number",
    "recordType": "string",
    "externalId": "string",
    "source": "string",
    "sourceCategory": ["string"],
    "depositDate": "string",
    "modifyDate": "string",
    "availableDate": "string",
    "status": "string",
    "depositorComments": ["string"],
    "relatedCompounds": ["string"]
}
```

## Error Handling
- Failed requests are logged with error messages
- Missing data fields are marked as "Unknown"
- Network errors are captured and recorded

## Configuration
- Default compound range: 1-100
- Default substance range: 1-5
- Modify ranges in main_pubchem.py as needed

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
MIT License