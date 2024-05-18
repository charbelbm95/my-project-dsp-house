import psycopg2

# Database connection parameters
host = "localhost"
dbname = "energy_output_db"
username = "postgres"
password = "12345678"

try:
    # Connect to the energy_output_db database
    conn = psycopg2.connect(dbname=dbname, user=username, password=password, host=host)
    cur = conn.cursor()
    print(f"Connected to the '{dbname}' database.")
    
    # Drop the existing predictions table if it exists
    try:
        print("Dropping the existing 'predictions' table if it exists...")
        cur.execute("DROP TABLE IF EXISTS predictions;")
        print("Table 'predictions' dropped successfully.")
    except Exception as e:
        print(f"An error occurred while dropping the table: {e}")
    
    # Create the new predictions table with the specified structure
    try:
        print("Creating the new 'predictions' table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY, 
                inputs TEXT, 
                prediction REAL,
                prediction_time TIMESTAMP,
                source TEXT
            );
        """)
        print("Table 'predictions' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
    
    cur.close()
    conn.close()
    print("Database connection closed.")
except Exception as e:
    print(f"An error occurred: {e}")
