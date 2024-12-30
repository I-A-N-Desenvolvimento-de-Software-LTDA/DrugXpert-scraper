// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('DrugXpert');

// Insert multiple documents in the collection.
db.getCollection('molecules').insertMany([
  {
    "moleculeName": "Aspirin",
    "smilesStructure": "CC(=O)OC1=CC=CC=C1C(O)=O",
    "molecularWeight": 180.16,
    "categoryUsage": "Pain reliever/NSAID"
  },
  {
    "moleculeName": "Caffeine",
    "smilesStructure": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "molecularWeight": 194.19,
    "categoryUsage": "Stimulant"
  },
  {
    "moleculeName": "Benzene",
    "smilesStructure": "C1=CC=CC=C1",
    "molecularWeight": 78.11,
    "categoryUsage": "Industrial solvent"
  },
  {
    "moleculeName": "Glucose",
    "smilesStructure": "C(C1C(C(C(C(O1)O)O)O)O)O",
    "molecularWeight": 180.16,
    "categoryUsage": "Energy source/sugar"
  },
  {
    "moleculeName": "Penicillin",
    "smilesStructure": "CC1(C2C(C(C(O2)N1C(=O)COC(=O)C)C)S)C=O",
    "molecularWeight": 334.39,
    "categoryUsage": "Antibiotic"
  },
  {
    "moleculeName": "Ibuprofen",
    "smilesStructure": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
    "molecularWeight": 206.29,
    "categoryUsage": "Anti-inflammatory"
  },
  {
    "moleculeName": "Ethanol",
    "smilesStructure": "CCO",
    "molecularWeight": 46.07,
    "categoryUsage": "Solvent/alcohol"
  },
  {
    "moleculeName": "Chloroform",
    "smilesStructure": "CCl3",
    "molecularWeight": 119.38,
    "categoryUsage": "Anesthetic"
  },
  {
    "moleculeName": "Acetone",
    "smilesStructure": "CC(=O)C",
    "molecularWeight": 58.08,
    "categoryUsage": "Solvent"
  },
  {
    "moleculeName": "Morphine",
    "smilesStructure": "C17H19NO3",
    "molecularWeight": 285.34,
    "categoryUsage": "Analgesic/opioid"
  },
  {
    "moleculeName": "Vitamin C",
    "smilesStructure": "C6H8O6",
    "molecularWeight": 176.12,
    "categoryUsage": "Antioxidant/nutrient"
  },
  {
    "moleculeName": "Nicotine",
    "smilesStructure": "CN1CCC2=C(C1)C=CN=C2",
    "molecularWeight": 162.23,
    "categoryUsage": "Stimulant"
  },
  {
    "moleculeName": "Methanol",
    "smilesStructure": "CO",
    "molecularWeight": 32.04,
    "categoryUsage": "Solvent/alcohol"
  },
  {
    "moleculeName": "Serotonin",
    "smilesStructure": "C10H12N2O",
    "molecularWeight": 176.21,
    "categoryUsage": "Neurotransmitter"
  },
  {
    "moleculeName": "Acetylcholine",
    "smilesStructure": "CC(=O)OCC[N+](C)(C)C",
    "molecularWeight": 146.21,
    "categoryUsage": "Neurotransmitter"
  },
  {
    "moleculeName": "Adrenaline",
    "smilesStructure": "C9H13NO3",
    "molecularWeight": 183.21,
    "categoryUsage": "Hormone/stimulant"
  },
  {
    "moleculeName": "Histamine",
    "smilesStructure": "C5H9N3",
    "molecularWeight": 111.15,
    "categoryUsage": "Neurotransmitter/immune response"
  },
  {
    "moleculeName": "Dopamine",
    "smilesStructure": "C8H11NO2",
    "molecularWeight": 153.18,
    "categoryUsage": "Neurotransmitter"
  },
  {
    "moleculeName": "Progesterone",
    "smilesStructure": "C21H30O2",
    "molecularWeight": 314.47,
    "categoryUsage": "Hormone"
  },
  {
    "moleculeName": "Estradiol",
    "smilesStructure": "C18H24O2",
    "molecularWeight": 272.38,
    "categoryUsage": "Hormone"
  },
  {
    "moleculeName": "Cholesterol",
    "smilesStructure": "C27H46O",
    "molecularWeight": 386.65,
    "categoryUsage": "Cell membrane component"
  },
  {
    "moleculeName": "Cortisone",
    "smilesStructure": "C21H28O5",
    "molecularWeight": 360.45,
    "categoryUsage": "Hormone/anti-inflammatory"
  },
  {
    "moleculeName": "Urea",
    "smilesStructure": "C(N)N=O",
    "molecularWeight": 60.06,
    "categoryUsage": "Nitrogen excretion"
  },
  {
    "moleculeName": "Hydrochloric acid",
    "smilesStructure": "Cl",
    "molecularWeight": 36.46,
    "categoryUsage": "Acid/base chemical"
  },
  {
    "moleculeName": "Nitroglycerin",
    "smilesStructure": "C3H5N3O9",
    "molecularWeight": 227.09,
    "categoryUsage": "Explosive/heart medication"
  },
  {
    "moleculeName": "Paracetamol",
    "smilesStructure": "CC(=O)NC1=CC=C(C=C1)O",
    "molecularWeight": 151.16,
    "categoryUsage": "Pain reliever/antipyretic"
  },
  {
    "moleculeName": "Methotrexate",
    "smilesStructure": "C20H22N8O5",
    "molecularWeight": 454.44,
    "categoryUsage": "Chemotherapy/immunosuppressant"
  }
]);
