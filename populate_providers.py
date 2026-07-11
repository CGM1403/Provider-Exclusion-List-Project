import pandas as pd
import sqlite3
import os
import sys

DB_PATH = "providers.db"
PROVIDERS_CSV = "my_providers.csv"

def populate_providers_table():
    """
    Reads provider data from a CSV file and loads it into the 'providers' table.
    This will REPLACE any existing data in the table.
    """
    if not os.path.exists(PROVIDERS_CSV):
        print(f"[!] ERROR: Provider data file not found at '{PROVIDERS_CSV}'.")
        print("[*] Please create this file and add your provider data to it.")
        sys.exit(1)

    try:
        conn = sqlite3.connect(DB_PATH)
        
        print(f"[*] Reading provider data from '{PROVIDERS_CSV}'...")
        df_providers = pd.read_csv(PROVIDERS_CSV, dtype=str)

        # Ensure all required columns are present
        required_cols = {'npi', 'first_name', 'last_name', 'organization_name', 'status'}
        if not required_cols.issubset(df_providers.columns):
            print(f"[!] ERROR: The CSV file must contain the following columns: {', '.join(required_cols)}")
            sys.exit(1)

        # Use if_exists='replace' to clear old data and insert the new list
        df_providers.to_sql('providers', conn, if_exists='replace', index=False)
        
        print(f"[+] Successfully loaded {len(df_providers)} records into the 'providers' table.")
        conn.close()
    except Exception as e:
        print(f"[!] An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    populate_providers_table()