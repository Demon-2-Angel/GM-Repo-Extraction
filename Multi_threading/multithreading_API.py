import pandas as pd
import os
import requests
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def create_mesh_run_dict(file_path: str, sheet_name: str) -> dict:
    """
    Creates a dictionary where the keys are 'Disease MESH ID' and the values are lists of 'Run ID' values.
    """
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=sheet_name)
    mesh_run_dict = df.groupby('Disease MESH ID')['Run ID'].apply(list).to_dict()
    return mesh_run_dict

def create_folder_if_not_exists(folder_path):
    """
    Create folder if it does not exist.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")


from tqdm.auto import tqdm

def scrape_and_save(run_id, folder_path, no_data_log="no_data_with_health.log"):
    """
    Scrapes data for a given run_id and saves it as a TSV file in the specified folder.
    """
    # Check if the Run ID is in the no_data.log
    if os.path.exists(no_data_log):
        with open(no_data_log, 'r') as log_file:
            if run_id in log_file.read().splitlines():
                tqdm.write(f"Skipping Run ID (No Data): {run_id}")
                return

    file_path = os.path.join(folder_path, f"{run_id}.tsv")
    if os.path.exists(file_path):
        tqdm.write(f"File already exists for Run ID: {run_id}")
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
        tqdm.write(f"Error {response_uid.status_code} while fetching UID for Run ID: {run_id}")
        return

    loaded_uid = response_uid.json().get('run', {}).get('loaded_uid')
    if not loaded_uid:
        tqdm.write(f"No data found for Run ID: {run_id}")
        with open(no_data_log, 'a') as log_file:
            log_file.write(f"{run_id}\n")
        return

    # Second API call to get relative abundance data
    url_data = 'https://gmrepo.humangut.info/api/getRelativeAbundanceByRunID/'
    headers_data = headers_uid
    data_data = {'loaded_uid': loaded_uid, 'taxon_level': 'species'}
    response_data = requests.post(url_data, headers=headers_data, json=data_data)

    if response_data.status_code != 200:
        tqdm.write(f"Error {response_data.status_code} while fetching data for Run ID: {run_id}")
        return

    df = pd.DataFrame(response_data.json())
    if not df.empty:
        df.to_csv(file_path, sep='\t', index=False)
        tqdm.write(f"Data saved for Run ID: {run_id}")
    else:
        tqdm.write(f"No data found for Run ID: {run_id}")
        with open(no_data_log, 'a') as log_file:
            log_file.write(f"{run_id}\n")


def process_run_ids_concurrently(mesh_run_dict, base_directory, max_workers=10):
    """
    Processes Run IDs in the dictionary concurrently using ThreadPoolExecutor.
    """
    for key, run_ids in mesh_run_dict.items():
        folder_path = os.path.join(base_directory, str(key))
        create_folder_if_not_exists(folder_path)

        print(f"Processing Mesh ID: {key}")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(scrape_and_save, run_id, folder_path): run_id
                for run_id in run_ids
            }
            for future in tqdm(as_completed(futures), total=len(run_ids), desc=f"Mesh ID {key}"):
                run_id = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing Run ID {run_id}: {e}")

# Example usage
file_path = "path to excel file"
sheet_name = 'Name of the sheet name'
mesh_run_dict = create_mesh_run_dict(file_path, sheet_name)
base_directory = "Directory where files needs to be downloaded"

# Process Run IDs concurrently
process_run_ids_concurrently(mesh_run_dict, base_directory, max_workers=30)
