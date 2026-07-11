import pandas as pd
import sqlite3
import os

# Define file paths
DB_PATH = "providers.db"
FED_FILE = "UPDATED.csv"
GA_FILE = "Department of Community health Office Of Inspector General List of Excluded Individuals and Entities as of July 1, 2026.xlsx"

def process_exclusions():
    # Ensure database exists/connects
    conn = sqlite3.connect(DB_PATH)
    
    # ---------------------------------------------------------
    # 1. PROCESS FEDERAL LEIE DATA (UPDATED.csv)
    # ---------------------------------------------------------
    print(f"[*] Processing Federal file: {FED_FILE}...")
    df_fed = pd.read_csv(FED_FILE, low_memory=False, dtype=str)
    
    # Select and rename columns to match our standard schema
    # Note: Using .get() in case specific columns vary slightly in your raw file
    df_fed_clean = df_fed[['NPI', 'LASTNAME', 'FIRSTNAME', 'BUSNAME', 'EXCLTYPE', 'EXCLDATE']].copy()
    df_fed_clean = df_fed_clean.rename(columns={
        'NPI': 'npi',
        'LASTNAME': 'last_name',
        'FIRSTNAME': 'first_name',
        'BUSNAME': 'business_name',
        'EXCLTYPE': 'exclusion_type',
        'EXCLDATE': 'exclusion_date'
    })
    
    # Clean up NPI: Federal data often uses '0' for missing NPIs
    df_fed_clean['source'] = 'Federal OIG'
    df_fed_clean['npi'] = df_fed_clean['npi'].apply(lambda x: None if x == '0' else x)

    # ---------------------------------------------------------
    # 2. PROCESS GEORGIA STATE DATA (.xlsx)
    # ---------------------------------------------------------
    print(f"[*] Processing Georgia State file: {GA_FILE}...")
    # Skip the first 2 rows because the actual data headers start on row 3
    df_ga = pd.read_excel(GA_FILE, sheet_name='Sheet1', skiprows=2, dtype=str)
    
    # Standardize GA columns
    df_ga_clean = df_ga[['NPI', 'LAST NAME', 'FIRST NAME', 'BUSINESS NAME', 'GENERAL', 'SANCDATE']].copy()
    df_ga_clean = df_ga_clean.rename(columns={
        'NPI': 'npi',
        'LAST NAME': 'last_name',
        'FIRST NAME': 'first_name',
        'BUSINESS NAME': 'business_name',
        'GENERAL': 'exclusion_type',
        'SANCDATE': 'exclusion_date'
    })
    
    df_ga_clean['source'] = 'Georgia OIG'

    # ---------------------------------------------------------
    # 3. COMBINE AND INSERT INTO DATABASE
    # ---------------------------------------------------------
    print("[*] Combining datasets and saving to database...")
    df_combined = pd.concat([df_fed_clean, df_ga_clean], ignore_index=True)
    
    # Load into the 'exclusions' table
    df_combined.to_sql('exclusions', conn, if_exists='replace', index=False)
    
    conn.close()
    print(f"[+] Ingestion complete! {len(df_combined)} total records loaded into 'exclusions' table.")

if __name__ == "__main__":
    process_exclusions()