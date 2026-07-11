# Provider Exclusion List Checker

## Overview

This project provides a set of Python scripts to build and check against a database of excluded healthcare providers. It helps healthcare organizations ensure compliance by identifying active providers in their system who are present on federal or state exclusion lists.

The system ingests data from the federal Office of Inspector General (OIG) List of Excluded Individuals and Entities (LEIE) and the Georgia state exclusion list, combines them into a unified SQLite database, and then checks a local list of providers against this database.

## Features

*   **Data Ingestion**: Processes and standardizes data from multiple sources (CSV and Excel).
*   **Federal & State Lists**: Includes support for the federal OIG list and the Georgia DCH OIG list.
*   **Database Storage**: Consolidates all exclusion records into a single, queryable SQLite database.
*   **Provider Screening**: Checks a list of active providers against the exclusion database using their National Provider Identifier (NPI).
*   **Reporting**: Generates a CSV report (`exclusion_risk_report.csv`) detailing any active providers found on an exclusion list.

## Prerequisites

*   Python 3.7+
*   The Python libraries listed in `requirements.txt`.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/CGM1403/Provider-Exclusion-List-Project
    cd Provider-Exclusion-List-Project
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Prepare Data Files:**
    Place the following data files in the root directory of the project:
    *   **Federal Data:** `UPDATED.csv` (Downloadable from OIG LEIE)
    *   **Georgia State Data:** `Department of Community health Office Of Inspector General List of Excluded Individuals and Entities as of July 1, 2026.xlsx` (or the latest version from the Georgia DCH website).

4.  **Prepare the Provider Database:**
    The `check_exclusions.py` script requires a table named `providers` to exist within the `providers.db` database. The ingestion script will create the database file, but you must populate the `providers` table yourself.

    The `providers` table must have at least the following columns:
    *   `npi` (TEXT): The provider's National Provider Identifier.
    *   `status` (TEXT): The provider's status (e.g., 'Active').

    You can use a tool like DB Browser for SQLite or a simple Python script to create and populate this table.

    **Example SQL to create the table:**
    ```sql
    CREATE TABLE providers (
        npi TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        organization_name TEXT,
        status TEXT NOT NULL
    );
    ```

## Usage

Follow these steps to run the project:

1.  **Ingest Exclusion Data:**
    Run the `ingest_exclusions.py` script to process the raw data files and build the `exclusions` table in the `providers.db` database.

    ```bash
    python ingest_exclusions.py
    ```
    This will create/replace the `exclusions` table with the latest data from your source files.

2.  **Check for Excluded Providers:**
    After ingesting the data and ensuring your `providers` table is populated, run the `check_exclusions.py` script.

    ```bash
    python check_exclusions.py
    ```
    *   If any of your 'Active' providers are found in the exclusion list, a summary will be printed to the console, and a detailed report named `exclusion_risk_report.csv` will be saved in the project directory.
    *   If no matches are found, a confirmation message will be printed.

## Project Structure

```
├── ingest_exclusions.py            # Script to process source files and populate the database.
├── check_exclusions.py             # Script to check active providers against the exclusion list.
├── providers.db                    # SQLite database (created by the scripts).
├── UPDATED.csv                     # Raw federal exclusion data (must be provided).
├── ...2026.xlsx                    # Raw Georgia exclusion data (must be provided).
├── exclusion_risk_report.csv       # Output report (generated if matches are found).
├── requirements.txt                # Python package dependencies.
└── README.md                       # This file.
```

## Future Improvements

*   **Automated Downloads**: Add functionality to automatically download the latest exclusion lists from their sources.
*   **Broader Matching**: Implement fuzzy name matching for providers who may be on an exclusion list but lack an NPI in the source data.
*   **Support for More States**: Extend the ingestion script to handle exclusion lists from other states.
*   **Web Interface**: Create a simple web front-end to run checks and view reports.

---
