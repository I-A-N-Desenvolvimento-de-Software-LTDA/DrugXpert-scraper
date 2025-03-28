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
            
            # Initialize values with defaults
            smiles_structure = "Unknown"
            inchi_string = "Unknown"
            inchi_key = "Unknown"
            molecular_formula = "Unknown"
            molecular_weight = "Unknown"
            drugbank_id = "Unknown"
            category_usage = "Unknown"
            description = "Unknown"
            cas_registry_number = "Unknown"
            unii = "Unknown"
            chebi_id = "Unknown"
            
            # Initialize physical properties
            xlogp3 = "Unknown"
            hydrogen_bond_donor_count = "Unknown"
            hydrogen_bond_acceptor_count = "Unknown"
            rotatable_bond_count = "Unknown"
            exact_mass = "Unknown"
            monoisotopic_mass = "Unknown"
            topological_polar_surface_area = "Unknown"
            heavy_atom_count = "Unknown"
            formal_charge = "Unknown"
            complexity = "Unknown"
            isotope_atom_count = "Unknown"
            defined_atom_stereocenter_count = "Unknown"
            undefined_atom_stereocenter_count = "Unknown"
            defined_bond_stereocenter_count = "Unknown"
            undefined_bond_stereocenter_count = "Unknown"
            covalently_bonded_unit_count = "Unknown"
            
            # Initialize metadata
            create_date = "Unknown"
            modify_date = "Unknown"
            
            # Additional identifiers
            hmdb_id = "Unknown"
            lipid_maps_id = "Unknown"
            nci_thesaurus_code = "Unknown"
            metabolomics_workbench_id = "Unknown"
            dsstox_id = "Unknown"
            wikidata = "Unknown"
            
            # Spectral data placeholders
            nmr_shifts_proton = []
            nmr_shifts_carbon = []
            mass_spec_peaks = ""
            
            # Additional properties
            melting_point = "Unknown"
            solubility = "Unknown"
            
            # Biological properties
            organism_presence = []
            biochemical_function = "Unknown"
            
            # Pharmacology fields
            mechanism = "Unknown"
            pharmacodynamics = "Unknown"
            absorption = "Unknown"
            route_of_elimination = "Unknown"
            indications_text = "Unknown"
            
            # Synonyms list
            synonyms = []
            
            sections = record.get("Section", [])
            for section in sections:
                # Names and Identifiers section
                if section.get("TOCHeading") == "Names and Identifiers":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Record Description":
                            for info in subsection.get("Information", []):
                                if info.get("Name") == "Record Description":
                                    try:
                                        description = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                        
                        elif subsection.get("TOCHeading") == "Computed Descriptors":
                            for subsubsection in subsection.get("Section", []):
                                if subsubsection.get("TOCHeading") == "SMILES":
                                    try:
                                        smiles_structure = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "InChI":
                                    try:
                                        inchi_string = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "InChIKey":
                                    try:
                                        inchi_key = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass

                        elif subsection.get("TOCHeading") == "Molecular Formula":
                            try:
                                molecular_formula = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                            except (IndexError, TypeError):
                                pass
                        
                        elif subsection.get("TOCHeading") == "Other Identifiers":
                            for identifier in subsection.get("Section", []):
                                if identifier.get("TOCHeading") == "DrugBank ID":
                                    try:
                                        drugbank_id = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif identifier.get("TOCHeading") == "CAS":
                                    try:
                                        cas_registry_number = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif identifier.get("TOCHeading") == "UNII":
                                    try:
                                        unii = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif identifier.get("TOCHeading") == "ChEBI ID":
                                    try:
                                        chebi_id = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif identifier.get("TOCHeading") == "HMDB ID":
                                    try:
                                        hmdb_id = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif identifier.get("TOCHeading") == "Lipid Maps ID (LM_ID)":
                                    try:
                                        lipid_maps_id = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif identifier.get("TOCHeading") == "NCI Thesaurus Code":
                                    try:
                                        nci_thesaurus_code = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif identifier.get("TOCHeading") == "Metabolomics Workbench ID":
                                    try:
                                        metabolomics_workbench_id = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif identifier.get("TOCHeading") == "DSSTox Substance ID":
                                    try:
                                        dsstox_id = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif identifier.get("TOCHeading") == "Wikidata":
                                    try:
                                        wikidata = identifier.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                        
                        elif subsection.get("TOCHeading") == "Synonyms":
                            for synonym_section in subsection.get("Section", []):
                                for info in synonym_section.get("Information", []):
                                    if "Value" in info and "StringWithMarkup" in info["Value"]:
                                        for synonym_data in info["Value"]["StringWithMarkup"]:
                                            if "String" in synonym_data and synonym_data["String"] not in synonyms and synonym_data["String"] != "":
                                                synonyms.append(synonym_data["String"])
                        
                        elif subsection.get("TOCHeading") == "Create Date":
                            for info in subsection.get("Information", []):
                                if "Value" in info and "DateISO8601" in info["Value"] and len(info["Value"]["DateISO8601"]) > 0:
                                    create_date = info["Value"]["DateISO8601"][0]
                        
                        elif subsection.get("TOCHeading") == "Modify Date":
                            for info in subsection.get("Information", []):
                                if "Value" in info and "DateISO8601" in info["Value"] and len(info["Value"]["DateISO8601"]) > 0:
                                    modify_date = info["Value"]["DateISO8601"][0]

                # Chemical and Physical Properties section
                elif section.get("TOCHeading") == "Chemical and Physical Properties":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Computed Properties":
                            for subsubsection in subsection.get("Section", []):
                                if subsubsection.get("TOCHeading") == "Molecular Weight":
                                    try:
                                        molecular_weight = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                        if molecular_weight == "Unknown":
                                            # Try to get the numeric value directly
                                            molecular_weight = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "XLogP3":
                                    try:
                                        xlogp3 = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Hydrogen Bond Donor Count":
                                    try:
                                        hydrogen_bond_donor_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Hydrogen Bond Acceptor Count":
                                    try:
                                        hydrogen_bond_acceptor_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Rotatable Bond Count":
                                    try:
                                        rotatable_bond_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Exact Mass":
                                    try:
                                        exact_mass = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                        if exact_mass == "Unknown":
                                            # Try to get the numeric value directly
                                            exact_mass = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Monoisotopic Mass":
                                    try:
                                        monoisotopic_mass = subsubsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                        if monoisotopic_mass == "Unknown":
                                            # Try to get the numeric value directly
                                            monoisotopic_mass = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Topological Polar Surface Area":
                                    try:
                                        topological_polar_surface_area = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Heavy Atom Count":
                                    try:
                                        heavy_atom_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Formal Charge":
                                    try:
                                        formal_charge = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Complexity":
                                    try:
                                        complexity = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Isotope Atom Count":
                                    try:
                                        isotope_atom_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Defined Atom Stereocenter Count":
                                    try:
                                        defined_atom_stereocenter_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Undefined Atom Stereocenter Count":
                                    try:
                                        undefined_atom_stereocenter_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Defined Bond Stereocenter Count":
                                    try:
                                        defined_bond_stereocenter_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Undefined Bond Stereocenter Count":
                                    try:
                                        undefined_bond_stereocenter_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                elif subsubsection.get("TOCHeading") == "Covalently-Bonded Unit Count":
                                    try:
                                        covalently_bonded_unit_count = subsubsection.get("Information", [{}])[0].get("Value", {}).get("Number", ["Unknown"])[0]
                                    except (IndexError, TypeError):
                                        pass
                                        
                        elif subsection.get("TOCHeading") == "Experimental Properties":
                            for exp_section in subsection.get("Section", []):
                                if exp_section.get("TOCHeading") == "Melting Point":
                                    try:
                                        melting_point = exp_section.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif exp_section.get("TOCHeading") == "Solubility":
                                    try:
                                        solubility = exp_section.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                
                # Spectral Information section
                elif section.get("TOCHeading") == "Spectral Information":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "1D NMR Spectra":
                            for nmr_section in subsection.get("Section", []):
                                if nmr_section.get("TOCHeading") == "1H NMR Spectra":
                                    for info in nmr_section.get("Information", []):
                                        if info.get("Name") == "Shifts [ppm]:Intensity":
                                            try:
                                                shifts = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                                if shifts and shifts != "Unknown":
                                                    nmr_data = {
                                                        "instrument": "Bruker", # Default if not specified
                                                        "solvent": "D2O",  # Default if not specified
                                                        "shifts": shifts
                                                    }
                                                    
                                                    # Look for other NMR metadata in the same section
                                                    for meta_info in nmr_section.get("Information", []):
                                                        if meta_info.get("Name") == "Instrument Type":
                                                            inst = meta_info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                                            if inst:
                                                                nmr_data["instrument"] = inst
                                                        elif meta_info.get("Name") == "Solvent":
                                                            solv = meta_info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                                            if solv:
                                                                nmr_data["solvent"] = solv
                                                        elif meta_info.get("Name") == "Frequency":
                                                            freq = meta_info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                                            if freq:
                                                                nmr_data["frequency"] = freq
                                                    
                                                    nmr_shifts_proton.append(nmr_data)
                                            except (IndexError, TypeError):
                                                pass
                                                
                                elif nmr_section.get("TOCHeading") == "13C NMR Spectra":
                                    for info in nmr_section.get("Information", []):
                                        if info.get("Name") == "Shifts [ppm]:Intensity":
                                            try:
                                                shifts = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                                if shifts and shifts != "Unknown":
                                                    nmr_data = {
                                                        "instrument": "Bruker", # Default if not specified
                                                        "solvent": "D2O",  # Default if not specified
                                                        "shifts": shifts
                                                    }
                                                    
                                                    # Look for other NMR metadata in the same section
                                                    for meta_info in nmr_section.get("Information", []):
                                                        if meta_info.get("Name") == "Instrument Type":
                                                            inst = meta_info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                                            if inst:
                                                                nmr_data["instrument"] = inst
                                                        elif meta_info.get("Name") == "Solvent":
                                                            solv = meta_info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                                            if solv:
                                                                nmr_data["solvent"] = solv
                                                    
                                                    nmr_shifts_carbon.append(nmr_data)
                                            except (IndexError, TypeError):
                                                pass
                                                
                        elif subsection.get("TOCHeading") == "Mass Spectrometry":
                            for ms_section in subsection.get("Section", []):
                                for info in ms_section.get("Information", []):
                                    if info.get("Name") == "Top 5 Peaks":
                                        try:
                                            peaks = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                            if peaks and peaks != "Unknown":
                                                mass_spec_peaks = peaks
                                        except (IndexError, TypeError):
                                            pass
                                    elif info.get("Name") == "Precursor m/z" and not mass_spec_peaks:
                                        try:
                                            peaks = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                            if peaks and peaks != "Unknown":
                                                mass_spec_peaks = peaks
                                        except (IndexError, TypeError):
                                            pass
                
                # Drug and Medication Information section
                elif section.get("TOCHeading") == "Drug and Medication Information":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Drug Indication":
                            try:
                                indications_text = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                            except (IndexError, TypeError):
                                pass
                
                # Pharmacology and Biochemistry section
                elif section.get("TOCHeading") == "Pharmacology and Biochemistry":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Pharmacodynamics":
                            try:
                                pharmacodynamics = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                            except (IndexError, TypeError):
                                pass
                        elif subsection.get("TOCHeading") == "Mechanism of Action":
                            try:
                                mechanism = subsection.get("Information", [{}])[0].get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                            except (IndexError, TypeError):
                                pass
                        elif subsection.get("TOCHeading") == "Absorption, Distribution and Excretion":
                            for info in subsection.get("Information", []):
                                if info.get("Name") == "Absorption":
                                    try:
                                        absorption = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
                                elif info.get("Name") == "Route of Elimination":
                                    try:
                                        route_of_elimination = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "Unknown")
                                    except (IndexError, TypeError):
                                        pass
            
            # Process organism presence data from Record Description
            if description != "Unknown":
                # Extract organism mentions from description
                organisms = []
                if "found in " in description.lower():
                    org_part = description.lower().split("found in ")[1].split(".")[0]
                    organisms = [o.strip() for o in org_part.split(",")]
                
                if "human metabolite" in description.lower():
                    organisms.append("Human metabolite")
                
                if organisms:
                    organism_presence = organisms
            
            # Extract biochemical function
            if description != "Unknown":
                biochemical_function = description
            
            # Determine if racemic based on the name or stereochemistry information
            is_racemic = False
            if "DL-" in molecule_name or undefined_atom_stereocenter_count != "Unknown" and int(undefined_atom_stereocenter_count) > 0:
                is_racemic = True
            
            # Organize data according to the format.json structure
            transformed_item = {
                "basicInfo": {
                    "type": source_type,
                    "moleculeName": molecule_name,
                    "recordNumber": record_number,
                    "source": "pubchem",
                    "drugBankId": drugbank_id,
                    "casRegistryNumber": cas_registry_number,
                    "unii": unii,
                    "chebiId": chebi_id,
                    "description": description
                },
                "identifiers": {
                    "pubChemCID": compound_id,
                    "wikidata": wikidata,
                    "hmdbID": hmdb_id,
                    "lipidMapsID": lipid_maps_id,
                    "nciThesaurusCode": nci_thesaurus_code,
                    "metabolomicsWorkbenchID": metabolomics_workbench_id,
                    "dssToxID": dsstox_id
                },
                "structure": {
                    "smilesStructure": smiles_structure,
                    "inchiString": inchi_string,
                    "inchiKey": inchi_key,
                    "molecularFormula": molecular_formula
                },
                "physicalProperties": {
                    "molecularWeight": molecular_weight,
                    "exactMass": exact_mass,
                    "monoisotopicMass": monoisotopic_mass,
                    "xlogp3": xlogp3,
                    "formalCharge": formal_charge,
                    "complexity": complexity,
                    "topologicalPolarSurfaceArea": topological_polar_surface_area,
                    "heavyAtomCount": heavy_atom_count,
                    "meltingPoint": melting_point,
                    "solubility": solubility
                },
                "bondInformation": {
                    "hydrogenBondDonorCount": hydrogen_bond_donor_count,
                    "hydrogenBondAcceptorCount": hydrogen_bond_acceptor_count,
                    "rotatableBondCount": rotatable_bond_count,
                    "covalentlyBondedUnitCount": covalently_bonded_unit_count
                },
                "stereochemistry": {
                    "definedAtomStereocenterCount": defined_atom_stereocenter_count,
                    "undefinedAtomStereocenterCount": undefined_atom_stereocenter_count,
                    "definedBondStereocenterCount": defined_bond_stereocenter_count,
                    "undefinedBondStereocenterCount": undefined_bond_stereocenter_count,
                    "isotopeAtomCount": isotope_atom_count,
                    "isRacemic": is_racemic
                },
                "pharmacology": {
                    "indications": {
                        "text": indications_text
                    },
                    "overview": description,
                    "mechanism": mechanism,
                    "pharmacodynamics": pharmacodynamics,
                    "absorption": absorption,
                    "routeOfElimination": route_of_elimination,
                    "classification": {
                        "meshPharmacological": []
                    }
                },
                "synonyms": synonyms,
                "spectralData": {
                    "nmr": {
                        "proton": nmr_shifts_proton,
                        "carbon": nmr_shifts_carbon
                    },
                    "massSpectrometry": {
                        "precursorMZ": "",
                        "topPeaks": mass_spec_peaks
                    }
                },
                "biologicalProperties": {
                    "organismPresence": organism_presence,
                    "biochemicalFunction": biochemical_function
                },
                "commercialAvailability": {
                    "regulatoryStatus": {
                        "approved": [],
                        "investigational": []
                    }
                },
                "classification": {},
                "metadata": {
                    "createDate": create_date,
                    "modifyDate": modify_date,
                    "dataSource": "PubChem"
                }
            }
            
            transformed_data.append(transformed_item)

    # Save final result
    with open(output_file, "w") as json_file:
        json.dump(transformed_data, json_file, indent=4)
    print(f"Final compound data saved to {output_file}")
 
if __name__ == "__main__":
    process_compound_data(1, 20, "final_pubchem_compound_data.json", "compound")


