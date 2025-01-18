"""
PubChem Data Processing Pipeline

This module serves as the main orchestrator for the PubChem data processing pipeline.
It coordinates the fetching and processing of both compound and substance data from
the PubChem database.

The pipeline consists of two main processes:
1. Compound data processing
2. Substance data processing

Each process includes:
- Data fetching from PubChem REST API
- Data transformation
- Final JSON file generation

Author: Israel Neto
Date: 2024
"""

from compound_pubchem import process_compound_data
from substance_pubchem import process_substance_data

def main():
    """
    Main orchestrator function that runs the complete data processing pipeline.
    
    This function coordinates:
    - Compound data processing (IDs 1-100)
    - Substance data processing (IDs 1-5)
    
    Output files:
    - final_pubchem_compound_data.json
    - final_pubchem_substance_data.json
    """
    
    # Process compound data
    print("Processing compound data...")
    process_compound_data(1, 100, "final_pubchem_compound_data.json", "compound")
    
    # Process substance data
    print("\nProcessing substance data...")
    process_substance_data(1, 5, "final_pubchem_substance_data.json", "substance")

if __name__ == "__main__":
    main()
