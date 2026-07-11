import sqlite3
import pandas as pd

def check_exclusions():
    conn = sqlite3.connect("providers.db")
    
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
        
    conn.close()

if __name__ == "__main__":
    check_exclusions()