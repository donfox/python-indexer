import psycopg2
from psycopg2 import sql

# Connect to the default 'postgres' database first to create a new database
conn = psycopg2.connect(dbname="postgres", user="donfox1", password="xofnod", host="localhost", port=5432)
conn.autocommit = True

cursor = conn.cursor()

# Check if the 'indexer_lite' database already exists

# cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}").format(sql.Identifier("postgres")))
cursor.execute("SELECT datname FROM pg_database WHERE datname='postgres';")

#database_exists = cursor.fetchone()
exists = cursor.fetchone() is not None

#if not database_exists:
if exists:
    # Execute SQL commands to create a new database named 'indexer_lite'
    cursor.execute("CREATE DATABASE postgres")

    # Commit the changes
    conn.commit()

    print("Database 'postgres' created successfully.")
else:
    print("Database 'postgres' already exists.")

# Close the connection to the 'postgres' database
conn.close()

# Now connect to the 'indexer_lite' database
conn = psycopg2.connect(dbname="postgres", user="donfox1", password="xofnod", host="localhost", port=5432)
conn.autocommit = True

# Create a cursor object to interact with the new database
cursor = conn.cursor()

# Perform any additional operations on the 'podtgres' database if needed

# Close the connection to the 'postgres' database
conn.close()