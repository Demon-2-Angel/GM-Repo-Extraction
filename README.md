# GM-Repo-Extraction

## Scraping Run IDs and Organizing Downloaded Files

This project automates downloading TSV files associated with specific `Run IDs` and organizes them into folders based on their corresponding `Mesh IDs`.

## Features

- Reads `Mesh ID` and `Run ID` pairs from an Excel file.
- Ensures a folder structure where:
  - Each `Mesh ID` is a main folder.
  - Each `Run ID` is saved as a `.tsv` file in its respective `Mesh ID` folder.
- Scrapes data using API calls for each `Run ID`.
- Automatically resumes from where it left off if interrupted by checking existing `.tsv` files.
- Processes `Run IDs` in batches of 5000 for efficiency.
- Implements error handling for failed API calls.

---

## Prerequisites

- Python 3.7 or later.
- Required libraries:
  - `pandas`
  - `requests`
  - `tqdm`

### Install Dependencies

Install the required Python libraries:

```
pip install pandas requests tqdm
```

## File Structure
Ensure the following file structure before running the script:

```
project/
│
├── Data/
│   └── Run_Ids - Except Health.xlsx   # Input Excel file containing 'Mesh ID' and 'Run ID' pairs
│
├── Scrap Here/                        # Base folder for downloading files
│
└── scrape_script.py                   # Python script
```

# Configuration

## Excel File

- The script reads the input from an Excel file (`Run_Ids - Except Health.xlsx`).
- **Expected columns**:
  - **`Disease MESH ID`**: Represents the `Mesh ID`.
  - **`Run ID`**: Represents the `Run ID`.

## Parameters

Set these parameters in the script:

```
python
file_path = r"path_to_your_excel_file.xlsx"
sheet_name = "Run_Ids - Except Health"
base_path = r"path_to_download_folder"
```

## How to Run

### Steps:

1. **Ensure all prerequisites are met:**
   - Install the required libraries.
   - Verify the structure of the input Excel file.

2. **Edit the parameters in the script:**
   - Update `file_path`, `sheet_name`, and `base_path` variables with your actual paths.

3. **Run the script:**
   ```
   python scrape_script.py
   ```
## How It Works

### Reads Input:
- Extracts `Mesh ID` and `Run ID` pairs from the Excel file.

### Folder Structure:
- Ensures a folder exists for each `Mesh ID`.

### Download TSV Files:
- For each `Run ID`:
  - Uses API calls to retrieve data.
  - Saves the retrieved data as a `.tsv` file in the corresponding `Mesh ID` folder.
  - Skips existing files to avoid duplicate downloads.

### Batch Processing:
- Processes `Run IDs` in batches of 5000 to optimize performance.

---

## Troubleshooting

### Common Issues

#### 1. API Call Fails
- Check the console output for the specific error code.
- Verify the website's API functionality.

#### 2. Missing Files
- Ensure the correct paths for the Excel file and base directory are specified.
- Check the console output for skipped or failed `Run ID`s.

---

## Future Enhancements
- Implement retry logic for failed API calls.
- Add functionality for detailed logging.
- Generate a summary report of successfully downloaded files and failed attempts.
