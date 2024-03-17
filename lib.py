"""
lib.py

This module contains utility functions for interacting with the database and processing block data.

Functions:
- updatePrevBlockHash: Updates the previous block hash in the database.
- createBlock: Creates or updates a block record in the database.

Author: [Your Name]
Date: [Current Date]
"""
import json
import datetime
import psycopg2

def updatePrevBlockHash(height, prev_block_hash, chain_id, cursor, db_connection):
    """
    Updates the hash of the previous block in the database.

    Args:
        height (int): The height of the block.
        prev_block_hash (str): The hash of the previous block.
        chain_id (str): The chain ID of the block.
        cursor (psycopg2.cursor): The cursor object for executing SQL queries.
        db_connection (psycopg2.connection): The connection object for the database.

    """
    print("  --- lib.updatePrevBlockHash() -----[1]")

    try:
        # Implement the logic to update the previous block hash
        query = """
            UPDATE blocks
            SET hash = %s
            WHERE id = (
                SELECT id
                FROM blocks
                WHERE chain_id = %s AND height = %s AND hash IS NULL
                ORDER BY timestamp DESC
                LIMIT 1
            );
        """
        values = (prev_block_hash, chain_id, height)
        
        with db_connection, db_connection.cursor() as cursor:
            cursor.execute(query, values)
            rows_affected = cursor.rowcount

        if rows_affected > 0:
            print(f"\tPrevious block hash updated successfully at height {height}")
        else:
            print(f"\tNo row found for updating previous block hash at height {height}")

    except psycopg2.Error as e:
        # Handle database-related errors
        print(f"Error updating previous block hash at height {height}: {e}")

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")


def createBlock(height, cursor, db_connection, hash='', timestamp='', tx_count=0, chain_id=''):
    """
    Creates or updates a block record in the database.

    Args:
        height (int): The height of the block.
        cursor (psycopg2.cursor): The cursor object for executing SQL queries.
        db_connection (psycopg2.connection): The connection object for the database.
        hash (str, optional): The hash of the block. Defaults to ''.
        timestamp (str, optional): The timestamp of the block. Defaults to ''.
        tx_count (int, optional): The transaction count of the block. Defaults to 0.
        chain_id (str, optional): The chain ID of the block. Defaults to ''.

    Returns:
        int: The ID of the created or updated block record.

    """
    print("  --- lib.createBlock() -----[2]")

    current_timestamp = datetime.datetime.utcnow()
    print(f"TimeSTPM : ", current_timestamp)

    try:
        # Check if the record already exists
        check_query = "SELECT id FROM blocks WHERE chain_id = %s AND hash = %s"
        cursor.execute(check_query, (chain_id, hash))
        existing_block = cursor.fetchone()

        if existing_block:
            # Perform an update if the record already exists
            update_query = """
                UPDATE blocks
                SET height = %s, timestamp = %s, tx_count = %s, updated_at = %s
                WHERE chain_id = %s AND hash = %s
                RETURNING id;
            """
            update_values = (height, timestamp, tx_count, current_timestamp, chain_id, hash)
            cursor.execute(update_query, update_values)
        else:
            # Perform an insert if the record doesn't exist
            insert_query = """
                INSERT INTO blocks (chain_id, hash, height, timestamp, tx_count, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """
            insert_values = (chain_id, hash, height, timestamp, tx_count, current_timestamp, current_timestamp)
            cursor.execute(insert_query, insert_values)

        row = cursor.fetchone()

        if row is not None:
            block_id = row[0]
            db_connection.commit()
            return block_id
        else:
            print(f'No row found for creating/updating block at height {height}')

    except psycopg2.Error as e:
        # Handle database-related errors
        print(f"Error creating/updating block at height {height}: {e}")

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")


def processTransactions(txs, block_id, chain_id):
    """
    Process transactions for a block and update the database.

    Args:
        txs (list): List of transaction strings to process.
        block_id (str): ID of the block.
        chain_id (str): ID of the chain.

    Returns:
        None
    """
    print("  --- lib.process_transactions() -----[3] {block_id}")

    # for tx in txs:
    #     tx_hash = hash_to_hex(tx)
    #     tx_record = create_transaction(block_id, tx_hash, chain_id)
    #     if tx_record:
    #         process_messages(tx, tx_record, chain_id)

def create_transaction(block_id, tx_hash, chain_id):
    print("  --- lib.create_transaction() -----[3] {block_id}")


def process_messages(tx, tx_record, chain_id):
    print("  --- lib.process_messages() -----[3] {block_id}")


# Convert a Base64 block hash to a hex block hash
def get_hex_block_hash_from_base64_block_hash(hash):
    """
    Hash data (SHA256) and return result in uppercase hex format.

    Args:
        hash (str): Base64 block hash to convert to hex format.

    Returns:
        str: Uppercase hex block hash.
    """
    decoded_bytes = bytearray.fromhex(hash)
    return decoded_bytes.hex().upper()









    
