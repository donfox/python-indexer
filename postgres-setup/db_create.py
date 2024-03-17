import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


conn = psycopg2.connect(dbname="indexer_lite", user="donfox1", password="xofnod", host="localhost", port=5432)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = conn.cursor()

# Create the 'blocks' table (1)
create_blocks_table_query = """
CREATE TABLE IF NOT EXISTS blocks (
    id         UUID DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    chain_id   VARCHAR(255) NOT NULL,
    height     INTEGER NOT NULL,
    hash       VARCHAR(255),
    tx_count   INTEGER NOT NULL,
    timestamp  TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);

ALTER TABLE blocks OWNER TO donfox1;

CREATE INDEX blocks_chain_id ON blocks (chain_id);
CREATE UNIQUE INDEX blocks_chain_id_hash ON blocks (chain_id, hash);
CREATE UNIQUE INDEX blocks_hash ON blocks (hash);

-- CREATE POLICY "Blocks are viewable by everyone" ON blocks
--     FOR SELECT
--     TO authenticated, anon
--     USING (true);

-- GRANT SELECT ON blocks TO anon;
-- GRANT SELECT ON blocks TO authenticated;
"""
cursor.execute(create_blocks_table_query)

# Commit changes for 'blocks' table
conn.commit()
conn.close()

conn = psycopg2.connect(dbname="indexer_lite", user="donfox1", password="xofnod", host="localhost", port=5432)
# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the 'contracts' table
create_contracts_table_query = """
CREATE TABLE IF NOT EXISTS contracts (
    id          UUID DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    chain_id    TEXT NOT NULL,
    name        TEXT,
    address     TEXT NOT NULL UNIQUE,
    type        TEXT,
    code_id     INTEGER,
    init_tx     TEXT,
    init_height INTEGER,
    created_by  TEXT,
    created_at  TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at  TIMESTAMP WITH TIME ZONE NOT NULL,
    deleted_at  TIMESTAMP WITH TIME ZONE
);

ALTER TABLE contracts OWNER TO donfox1;

CREATE INDEX contracts_chain_id ON contracts (chain_id);
CREATE INDEX contracts_name ON contracts (name);
CREATE INDEX contracts_chain_id_name ON contracts (chain_id, name);
CREATE INDEX contracts_chain_id_address ON contracts (chain_id, address);
CREATE INDEX contracts_chain_id_created_by ON contracts (chain_id, created_by);
CREATE UNIQUE INDEX contracts_address ON contracts (address);
"""
cursor.execute(create_contracts_table_query)
conn.commit()
conn.close()

conn = psycopg2.connect(dbname="indexer_lite", user="donfox1", password="xofnod", host="localhost", port=5432)
cursor = conn.cursor()

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the 'addresses' table
create_addresses_table_query = """
CREATE TABLE IF NOT EXISTS addresses (
    id         UUID DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    chain_id   TEXT NOT NULL,
    address    TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);

ALTER TABLE addresses OWNER TO donfox1;

CREATE UNIQUE INDEX addresses_address ON addresses (address);
CREATE UNIQUE INDEX addresses_chain_id_address ON addresses (chain_id, address);
"""
cursor.execute(create_addresses_table_query)
conn.commit()
conn.close()

conn = psycopg2.connect(dbname="indexer_lite", user="donfox1", password="xofnod", host="localhost", port=5432)
cursor = conn.cursor()

# Create the 'transactions' table (2)
create_transactions_table_query = """
CREATE TABLE IF NOT EXISTS transactions (
    id         UUID DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    chain_id   TEXT NOT NULL,
    block_id   UUID NOT NULL REFERENCES blocks ON UPDATE CASCADE ON DELETE CASCADE,
    tx_hash    TEXT NOT NULL UNIQUE,
    msg_count  INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);

ALTER TABLE transactions OWNER TO donfox1;

CREATE UNIQUE INDEX transactions_chain_id_tx_hash ON transactions (chain_id, tx_hash);
CREATE INDEX transactions_chain_id ON transactions (chain_id);
CREATE UNIQUE INDEX transactions_tx_hash ON transactions (tx_hash);
"""

cursor.execute(create_transactions_table_query)

# Commit changes for 'transactions' table.
conn.commit()
conn.close()

conn = psycopg2.connect(dbname="indexer_lite", user="donfox1", password="xofnod", host="localhost", port=5432)
cursor = conn.cursor()

# Create the 'messages' table (3)
create_messages_table_query = """
CREATE TABLE IF NOT EXISTS messages (
    id             UUID DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    chain_id       VARCHAR(255) NOT NULL,
    transaction_id UUID NOT NULL REFERENCES transactions ON UPDATE CASCADE ON DELETE CASCADE,
    type           VARCHAR(255) NOT NULL,
    sender         VARCHAR(255) NOT NULL,
    contract       VARCHAR(255) NOT NULL,
    contract_id    UUID NOT NULL REFERENCES contracts,
    msg            JSONB NOT NULL,
    created_at     TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at     TIMESTAMP WITH TIME ZONE NOT NULL,
    deleted_at     TIMESTAMP WITH TIME ZONE
);

ALTER TABLE messages OWNER TO donfox1;

CREATE INDEX messages_chain_id ON messages (chain_id);
CREATE INDEX messages_type ON messages (type);
CREATE INDEX messages_sender ON messages (sender);
CREATE INDEX messages_contract ON messages (contract);
CREATE INDEX messages_chain_id_sender ON messages (chain_id, sender);
CREATE INDEX messages_chain_id_contract ON messages (chain_id, contract);
"""
cursor.execute(create_messages_table_query)

# Commit the changes for the 'messages' table
conn.commit()
conn.close()

conn = psycopg2.connect(dbname="indexer_lite", user="donfox1", password="xofnod", host="localhost", port=5432)
cursor = conn.cursor()

# Create the 'actions' table (4)
create_table_query = """
CREATE TABLE IF NOT EXISTS actions (
    id         UUID DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    message_id UUID NOT NULL REFERENCES messages ON UPDATE CASCADE ON DELETE CASCADE,
    chain_id   TEXT NOT NULL,
    name       TEXT NOT NULL,
    body       JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);

ALTER TABLE actions OWNER TO donfox1;

CREATE INDEX actions_chain_id ON actions (chain_id);
CREATE INDEX actions_name ON actions (name);
CREATE INDEX actions_chain_id_name ON actions (chain_id, name);
"""
cursor.execute(create_table_query)

# Commit the changes
conn.commit()
conn.close()

