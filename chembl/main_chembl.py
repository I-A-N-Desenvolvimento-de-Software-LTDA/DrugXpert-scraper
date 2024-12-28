import requests
import json

def fetch_chembl_data():
    url = "https://www.ebi.ac.uk/chembl/interface_api/es_proxy/es_data/get_es_document/chembl_molecule/CHEMBL4443036?source=_metadata.compound_generated.image_file%2Cmolecule_structures"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()

                with open("chembl_data.json", "w") as json_file:
                    json.dump(data, json_file, indent=4)

                print("Os dados foram salvos em 'chembl_data.json'.")
            except json.JSONDecodeError:
                print("Erro ao decodificar JSON. Resposta bruta:")
                print(response.text)
        else:
            print(f"Erro na requisição. Código de status: {response.status_code}")
    except requests.RequestException as e:
        print(f"Ocorreu um erro ao acessar a API: {e}")

if __name__ == "__main__":
    fetch_chembl_data()