import psycopg2

# Database connection parameters
host = "localhost"
dbname = "energy_output_db"
username = "postgres"
password = "12345678"

try:
    # Connect to the energy_output_db database
    print("Connecting to the database...")
    conn = psycopg2.connect(dbname=dbname, user=username, password=password, host=host)
    cur = conn.cursor()
    print(f"Connected to the '{dbname}' database.")
    
    # List all tables
    print("Listing all tables in the database...")
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    tables = cur.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])
    
    # Describe the predictions_tbl table
    print("Describing the 'predictions_tbl' table...")
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'predictions_tbl';
    """)
    columns = cur.fetchall()
    print("\nStructure of the 'predictions_tbl' table:")
    for column in columns:
        print(f"{column[0]}: {column[1]}")
    
    cur.close()
    conn.close()
    print("Database connection closed.")
except Exception as e:
    print(f"An error occurred: {e}")
