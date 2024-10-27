import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


host = "localhost"
default_dbname = "postgres"
username = "postgres"
password = "12345678" 
target_dbname = "energy_output_db"


conn = psycopg2.connect(dbname=default_dbname, user=username, password=password, host=host)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


cur = conn.cursor()


try:
    cur.execute(f"CREATE DATABASE {target_dbname};")
    print(f"Database '{target_dbname}' created successfully.")
except psycopg2.errors.DuplicateDatabase:
    print(f"Database '{target_dbname}' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cur.close()
    conn.close()


conn = psycopg2.connect(dbname=target_dbname, user=username, password=password, host=host)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()


try:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions_tbl (
            id INTEGER PRIMARY KEY, 
                inputs TEXT, 
                prediction REAL,
                prediction_time TIMESTAMP,
                source TEXT
            );
    """)
    print("Table 'predictions_tbl' created successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

cur.close()
conn.close()
