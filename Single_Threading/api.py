import pandas as pd
import os
import requests
from tqdm.auto import tqdm

def create_mesh_run_dict(file_path: str, sheet_name: str) -> dict:
    """
    Creates a dictionary where the keys are 'Disease MESH ID' and the values are lists of 'Run ID' values.
    
    Parameters:
        file_path (str): The path to the Excel file.
        sheet_name (str): The name of the sheet containing the data.

    Returns:
        dict: A dictionary with 'Disease MESH ID' as keys and lists of 'Run ID' as values.
    """
    # Load the Excel file and the specified sheet
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Create the dictionary
    mesh_run_dict = df.groupby('Disease MESH ID')['Run ID'].apply(list).to_dict()
    
    return mesh_run_dict

def display_dictionary(dictionary: dict):
    """
    Displays each key-value pair in the dictionary in a formatted way.

    Parameters:
        dictionary (dict): The dictionary to display.
    """
    for key, value in dictionary.items():
        print(f"Mesh ID: {key}")
        print(f"Run IDs: {', '.join(value)}\n")

def create_folders_from_keys(dictionary: dict, base_path: str):
    """
    Creates a folder for each key in the dictionary.

    Parameters:
        dictionary (dict): The dictionary where each key will be used as a folder name.
        base_path (str): The base directory where folders will be created.
    """
    # Ensure the base path exists
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # Create folders for each key in the dictionary
    for key in dictionary.keys():
        folder_path = os.path.join(base_path, str(key))
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created: {folder_path}")

def create_folder_if_not_exists(folder_path):
    """
    Create folder if it does not exist.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

def scrape_and_save(run_id, folder_path, no_data_log="no_data.log"):
    """
    Scrapes data for a given run_id and saves it as a TSV file in the specified folder.
    """
    # Check if the Run ID is in the no_data.log
    if os.path.exists(no_data_log):
        with open(no_data_log, 'r') as log_file:
            if run_id in log_file.read().splitlines():
                print(f"Skipping Run ID (No Data): {run_id}")
                return

    file_path = os.path.join(folder_path, f"{run_id}.tsv")
    if os.path.exists(file_path):
        print(f"File already exists for Run ID: {run_id}")
        return  # Skip if the file already exists

    # First API call to get loaded_uid
    url_uid = 'https://gmrepo.humangut.info/api/getRunDetailsByRunID/'
    headers_uid = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0'
    }
    data_uid = {"run_id": run_id}
    response_uid = requests.post(url_uid, headers=headers_uid, json=data_uid)
    
    if response_uid.status_code != 200:
        print(f"Error {response_uid.status_code} while fetching UID for Run ID: {run_id}")
        return
    
    loaded_uid = response_uid.json().get('run', {}).get('loaded_uid')
    if not loaded_uid:
        print(f"No data found for Run ID: {run_id}")
        # Log the Run ID in no_data.log
        with open(no_data_log, 'a') as log_file:
            log_file.write(f"{run_id}\n")
        return
    
    # Second API call to get relative abundance data
    url_data = 'https://gmrepo.humangut.info/api/getRelativeAbundanceByRunID/'
    headers_data = headers_uid  # Same headers
    data_data = {
        'loaded_uid': loaded_uid,
        'taxon_level': 'species'
    }
    response_data = requests.post(url_data, headers=headers_data, json=data_data)
    
    if response_data.status_code != 200:
        print(f"Error {response_data.status_code} while fetching data for Run ID: {run_id}")
        return
    
    # Save data as TSV
    df = pd.DataFrame(response_data.json())
    if not df.empty:
        df.to_csv(file_path, sep='\t', index=False)
        print(f"Data saved for Run ID: {run_id}")
    else:
        print(f"No data found for Run ID: {run_id}")
        # Log the Run ID in no_data.log
        with open(no_data_log, 'a') as log_file:
            log_file.write(f"{run_id}\n")

def process_run_ids(mesh_run_dict, base_directory):
    """
    Processes Run IDs in the dictionary.
    Creates folders for keys and scrapes data for Run IDs in batches of 5000.
    """
    for key, run_ids in mesh_run_dict.items():
        folder_path = os.path.join(base_directory, str(key))
        create_folder_if_not_exists(folder_path)
        
        # Process Run IDs in batches of 5000
        for i in range(0, len(run_ids), 5000):
            batch = run_ids[i:i + 5000]
            print(f"Processing batch {i//5000 + 1} for Mesh ID: {key}")
            for run_id in tqdm(batch, desc=f"Scraping for Mesh ID {key}"):
                scrape_and_save(run_id, folder_path)


# Example usage
file_path = "path to excel file"
sheet_name = 'Name of the sheet name'
mesh_run_dict = create_mesh_run_dict(file_path, sheet_name)
base_directory = "Directory where files needs to be downloaded"

# Create folders
create_folders_from_keys(mesh_run_dict, base_directory)
process_run_ids(mesh_run_dict, base_directory)