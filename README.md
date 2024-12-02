# GM-Repo-Extraction
## Scraping Run IDs and Organizing Downloaded Files

This project automates the process of downloading TSV files associated with specific `Run IDs` and organizes them into folders based on their corresponding `Mesh IDs`.

## Features

- Reads `Mesh ID` and `Run ID` pairs from an Excel file.
- Ensures a folder structure where:
  - Each `Mesh ID` is a main folder.
  - Each `Run ID` is a subfolder under its respective `Mesh ID`.
- Scrapes the web to download TSV files for each `Run ID` from the provided URL.
- Saves the downloaded TSV files in their respective `Run ID` folders.
- Implements multithreading for faster downloads.
- Runs in headless mode for improved performance.

---

## Prerequisites

- Python 3.7 or later.
- Firefox browser installed.
- GeckoDriver for Selenium (compatible with your Firefox version). - https://github.com/mozilla/geckodriver/releases
- Check Firefox and GeckoDriver Compatibility Here - https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html

### Install Dependencies

Install the required Python libraries:

```
bash
pip install pandas selenium
```

## Download GeckoDriver
Download GeckoDriver from the official releases page and add it to your system PATH or specify its location in the script.

## File Structure
Ensure the following file structure before running the script:

```
project/
│
├── Data/
│   └── Run_Ids - Except Health.xlsx   # Input Excel file containing 'Mesh ID' and 'Run ID' pairs
│
├── Scrap Here/                         # Base folder for downloading files
│
└── scrape_script.py                   # Python script
```

## Configuration

### Excel File
- The script reads the input from an Excel file (`Run_Ids - Except Health.xlsx`).
- **Expected columns**:
  - **`Disease MESH ID`**: Represents the `Mesh ID`.
  - **`Run ID`**: Represents the `Run ID`.

### Parameters
Set these parameters in the script:

- **File Path**: Path to the Excel file containing `Mesh ID` and `Run ID` pairs.
- **Base Path**: Directory where files will be organized.
- **Firefox Binary Path**: Path to the Firefox browser binary.
- **Base URL**: The base URL for accessing `Run ID` pages.

---

## How to Run

### Ensure the Prerequisites:
1. Install required libraries.
2. Verify Firefox and GeckoDriver setup.

### Edit Parameters:
Update the following variables in the script:
```
python
file_path = r"path_to_your_excel_file.xlsx"
sheet_name = "Run_Ids - Except Health"
base_path = r"path_to_download_folder"
firefox_binary_path = r"path_to_firefox_binary"
base_url = "https://gmrepo.humangut.info/data/run/"
```

## How It Works

### Reads Input:
- Extracts `Mesh ID` and `Run ID` pairs from the Excel file.

### Folder Structure:
- Ensures a folder for each `Mesh ID` and a subfolder for each `Run ID`.

### Download TSV Files:
- Navigates to the URL for each `Run ID`.
- Triggers the download of the associated TSV file.
- Moves the downloaded file into the corresponding `Run ID` folder.

### Multithreading:
- Downloads files concurrently to improve performance.

---

## Troubleshooting

### Common Issues

#### 1. GeckoDriver Not Found
- Ensure the GeckoDriver binary is added to your system PATH or specify its full path in the script:
  ```
  python
  service = Service(r"path_to_geckodriver")
  ```
#### 2. Headless Mode Fails
If the headless mode doesn't work:
Set options.headless = False to debug with a visible browser window.
#### 3. Missing Files
Check the console output for errors.
Verify the website’s behavior in a normal browser for compatibility issues.

### Future Enhancements
- Implement retry logic for failed downloads.
- Add support for other browsers like Chrome.
- Generate a summary report of downloaded files.
