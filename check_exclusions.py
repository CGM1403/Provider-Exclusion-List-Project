import sqlite3
import pandas as pd
import sys

def check_exclusions():
    conn = sqlite3.connect("providers.db")
    cursor = conn.cursor()
    
    # First, check if the 'providers' table actually exists in the database.
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='providers'")
    if cursor.fetchone() is None:
        print("[!] ERROR: The 'providers' table was not found in the database (providers.db).")
        print("[*] The 'ingest_exclusions.py' script only creates the 'exclusions' table.")
        print("[*] You must create and populate the 'providers' table with your own provider data before running this check.")
        print("[*] Please see the 'Prepare the Provider Database' section in README.md for instructions.")
        conn.close()
        sys.exit(1) # Exit the script with an error status

    # Second, check if the 'providers' table is empty.
    cursor.execute("SELECT COUNT(*) FROM providers")
    if cursor.fetchone()[0] == 0:
        print("[!] WARNING: The 'providers' table exists but is empty.")
        print("[*] No providers were checked against the exclusion list.")
        print("[*] You must populate the 'providers' table with your own provider data to perform a check.")
        print("[*] Please see the 'Prepare the Provider Database' section in README.md for instructions.")
        conn.close()
        sys.exit(0) # Exit gracefully

    # This query joins your providers table with the new exclusions table
    # It looks for matches based on the NPI number
    query = """
    SELECT 
        p.npi, 
        p.first_name, 
        p.last_name, 
        p.organization_name, 
        e.exclusion_type, 
        e.exclusion_date, 
        e.source
    FROM providers p
    JOIN exclusions e ON p.npi = e.npi
    WHERE p.status = 'Active';
    """
    
    df_results = pd.read_sql_query(query, conn)
    
    if not df_results.empty:
        print(f"[!] ALERT: Found {len(df_results)} active providers on the exclusion list!")
        print(df_results)
        # Optionally save this to a report file
        df_results.to_csv("exclusion_risk_report.csv", index=False)
    else:
        print("[*] No active providers found on the exclusion list.")
        
    conn.close() # Connection is closed in all paths

if __name__ == "__main__":
    check_exclusions()