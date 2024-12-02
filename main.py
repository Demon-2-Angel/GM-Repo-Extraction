import os
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

# Enable debugging output
LOGGER.setLevel(logging.DEBUG)

def create_mesh_run_dict(file_path: str, sheet_name: str) -> dict:
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=sheet_name)
    return df.groupby('Disease MESH ID')['Run ID'].apply(list).to_dict()


def ensure_folder_structure(base_path: str, mesh_id: str, run_id: str) -> str:
    mesh_folder_path = os.path.join(base_path, mesh_id)
    run_folder_path = os.path.join(mesh_folder_path, run_id)
    os.makedirs(run_folder_path, exist_ok=True)
    return run_folder_path


def wait_for_download(download_dir, timeout=30):
    end_time = time.time() + timeout
    initial_files = set(os.listdir(download_dir))
    while time.time() < end_time:
        current_files = set(os.listdir(download_dir))
        new_files = current_files - initial_files
        if new_files:
            return os.path.join(download_dir, new_files.pop())
        time.sleep(1)
    return None


def download_tsv(base_url, run_id, firefox_binary_path, download_dir):
    options = Options()
    options.binary_location = firefox_binary_path
    options.headless = True  # Enable headless mode
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    options.set_preference("dom.webdriver.enabled", False)  # Avoid detection as WebDriver
    options.set_preference("dom.webnotifications.enabled", False)  # Disable notifications
    options.set_preference("media.navigator.enabled", True)  # Enable media navigation
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/tab-separated-values")

    service = Service(r"C:\path_to_geckodriver\geckodriver.exe")
    driver = webdriver.Firefox(service=service, options=options)
    test_url = f"{base_url}{run_id}"

    try:
        driver.get(test_url)
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@ng-click=\"downloadRelativeAbundanceByRunID( run, 'species' )\"]")))
        element.click()
        downloaded_file = wait_for_download(download_dir)
        return downloaded_file
    except Exception as e:
        print(f"Error processing Run ID {run_id}: {e}")
        return None
    finally:
        driver.quit()


def scrape_run_data(mesh_id, run_id, base_url, base_path, firefox_binary_path):
    run_folder_path = ensure_folder_structure(base_path, str(mesh_id), str(run_id))
    existing_files = os.listdir(run_folder_path)

    if f"{run_id}.tsv" not in existing_files:
        downloaded_file = download_tsv(base_url, run_id, firefox_binary_path, base_path)
        if downloaded_file:
            final_path = os.path.join(run_folder_path, os.path.basename(downloaded_file))
            os.rename(downloaded_file, final_path)
            print(f"File moved to: {final_path}")
        else:
            print(f"Failed to download file for Run ID {run_id}")


def scrape_mesh_run_data(base_url, mesh_run_dict, base_path, firefox_binary_path, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for mesh_id, run_ids in mesh_run_dict.items():
            for run_id in run_ids:
                executor.submit(scrape_run_data, mesh_id, run_id, base_url, base_path, firefox_binary_path)


# Parameters
file_path = r'C:\Users\aniru\Machine Learning\Internships\Virturis Wellness\Task 1 - Scraping\SQL Scrap - Run IDs\Run_Ids - Except Health.xlsx'
sheet_name = 'Run_Ids - Except Health'
base_path = r"C:\Users\aniru\Machine Learning\Internships\Virturis Wellness\Task 1 - Scraping\supertums"
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
base_url = "https://gmrepo.humangut.info/data/run/"

mesh_run_dict = create_mesh_run_dict(file_path, sheet_name)

# Run the scraper with multithreading and headless mode
scrape_mesh_run_data(base_url, mesh_run_dict, base_path, firefox_binary_path, max_workers=5)
