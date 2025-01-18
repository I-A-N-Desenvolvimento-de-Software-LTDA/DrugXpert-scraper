from compound_pubchem import process_compound_data
from substance_pubchem import process_substance_data

def main():
    """Main function to orchestrate both compound and substance data processing"""
    
    # Process compound data
    print("Processing compound data...")
    process_compound_data(1, 100, "final_pubchem_compound_data.json", "compound")
    
    # Process substance data
    print("\nProcessing substance data...")
    process_substance_data(1, 5, "final_pubchem_substance_data.json", "substance")

if __name__ == "__main__":
    main()
