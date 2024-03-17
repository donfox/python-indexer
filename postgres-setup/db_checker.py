import psycopg2
#
# Check if database exists.
#
conn = psycopg2.connect(dbname="indexer_lite", user="donfox1", password="xofnod", host="localhost", port=5432)
cursor = conn.cursor()

cursor.execute("SELECT datname FROM pg_database WHERE datname='indexer_lite';")
exists = cursor.fetchone() is not None

if exists:
    print("Database 'indexer_lite' exists.")
else:
    print("Database 'indexer_lite' does not exist.")
    
conn.close()
