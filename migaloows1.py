 # -----------------------------------------------------------------------------------------------
  # block_indexer.py
  #
  # Description:
  #
  # This application reads a series of block files from an online blockchain provider, tests them 
  # for well-formedness( ), and then extracts certain information recording that in a local postgres 
  # database. 
  #
  # WebSocket Server:
  #   URL: 'ws://116.202.143.93:26657/websocket'
  #
  #  Author: [Your Name]
  #  Date: [Current Date]
  # -----------------------------------------------------------------------------------------------
import os
import sys
import json
import requests
import psycopg2

from lib import updatePrevBlockHash, createBlock, processTransactions

MIN_FILE_SIZE = 35000
START_HEIGHT = 4191691
NUM_BLOCKS = 75
BLOCK_COUNT = START_HEIGHT + NUM_BLOCKS
LOCAL_BLOCK_DIR = './tendermint-blocks-repo'

BLOCK_CHAIN_URL = "http://116.202.143.93:1317/cosmos/base/tendermint/v1beta1/blocks/{}"
# DECODER_URL = "https://phoenix-lcd.terra.dev/cosmos/tx/v1beta1/decode"

DB_CONFIG = {
    "database": "indexer_lite",
    "user": "donfox1",
    "password": "xofnod",
    "host": "localhost",
    "port": "5432"
}

def inform_database(data, txs, db_connection, cursor):
    """
    Update the database with information from a block and its transactions.

    Args:
        data (str): JSON string containing block data.
        txs (list): List of transactions.
        db_connection (psycopg2.extensions.connection): Database connection object.
        cursor (psycopg2.extensions.cursor): Database cursor object.

    Returns:
        None
    """
    try:
        data = json.loads(str(data))

        if 'block' in data and 'header' in data['block']:
            block = data['block']
            block_data = block['data']
            header = block['header']
            height = header['height']
            prev_block_hash = header['last_block_id']['hash']
            chain_id = header['chain_id']

            updatePrevBlockHash(height, prev_block_hash, chain_id, cursor, db_connection)
            block_record = createBlock(int(height), cursor, db_connection, '', header["time"], \
                                        len(block["data"]["txs"]), chain_id)
            print(f"\n\tBLOCK_RECORD ret : ", block_record)

            # Uncomment the line below if you want to process transactions
            processTransactions(txs, block_record, chain_id)
        else:
            print("No 'block' key or 'header' key in block")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {str(e)}")


def download_and_check_blocks(db_connection, cursor):
    """
    Downloads blockchain blocks from the specified range, verifies their integrity,
    and stores them locally and in the database.

    Args:
        db_connection: Database connection object.
        cursor: Cursor object for executing SQL queries.

    Returns:
        None
    """
    for cnt, BLOCK_name in enumerate(range(START_HEIGHT, BLOCK_COUNT), 1):
        block_url = BLOCK_CHAIN_URL.format(BLOCK_name)
        response = requests.get(block_url)
        
        if response.status_code != 200:
            print(f"Error: Failed to fetch block {BLOCK_name}. Status code: {response.status_code}")
            continue
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"Error: {BLOCK_name} - JSON decoding error: {str(e)}")
            continue

        try:
            block = data.get('block')
            if not block:
                raise ValueError("Block data not found in response")
        except ValueError as e:
            print(f"Error: {BLOCK_name} - {str(e)}")
            continue

        txs = block['data']['txs']
        block_data = json.dumps(data, indent=2)
        block_size = len(block_data)

        # Skip blocks without transactions or too small
        if not isinstance(txs, list) or len(txs) == 0 or block_size <= MIN_FILE_SIZE:
            continue

        # Inform database
        inform_database(block_data, txs, db_connection, cursor)

        # Save block data locally
        file_path = os.path. join(LOCAL_BLOCK_DIR, str(BLOCK_name))
        with open(file_path, "w", buffering=1024 * 1024) as file:
            file.write(block_data)

        # Decode transactions (if needed)
        # decode_transaction(file_path, BLOCK_name, txs)


if __name__ == '__main__':
    try:
        # Attempt to establish a connection to the database
        db_connection = psycopg2.connect(**DB_CONFIG)
        cursor = db_connection.cursor()

        # Execute the main function
        download_and_check_blocks(db_connection, cursor)

    except psycopg2.Error as e:
        # Handle database-related errors
        print(f"Failed to connect with DB: {e}")

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")

    finally:
        # Ensure database connection and cursor are closed
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

    print('\tDONE\n')
    sys.exit()
