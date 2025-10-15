"""Data Loader 
Loads JSON events from files into MySQL staging tables
"""

import json
import os
import pymysql
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create database connection"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME_STAGING', 'ecommerce_staging'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('[SUCCESS] Connected to MySQL database')
        return connection
    except Exception as e:
        print(f'[ERROR] Could not connect to database: {e}')
        return None

def insert_event(cursor, event):
    """Insert a single event into staging table"""
    
    # Parse timestamp
    timestamp = datetime.fromisoformat(event['timestamp'])
    
    # Base fields for all events
    sql = """
        INSERT INTO staging_events (
            event_id, event_type, user_id, session_id, timestamp,
            page_url, device, browser,
            product_id, product_name, price, quantity,
            order_id, total_amount, items_count, payment_method,
            shipping_city, shipping_state, shipping_zip,
            rating, review_text, verified_purchase
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s
        )
    """
    
    # Extract shipping address if exists
    shipping = event.get('shipping_address', {})
    
    values = (
        event.get('event_id'),
        event.get('event_type'),
        event.get('user_id'),
        event.get('session_id'),
        timestamp,
        event.get('page_url'),
        event.get('device'),
        event.get('browser'),
        event.get('product_id'),
        event.get('product_name'),
        event.get('price'),
        event.get('quantity'),
        event.get('order_id'),
        event.get('total_amount'),
        event.get('items_count'),
        event.get('payment_method'),
        shipping.get('city'),
        shipping.get('state'),
        shipping.get('zip'),
        event.get('rating'),
        event.get('review_text'),
        event.get('verified_purchase')
    )
    
    cursor.execute(sql, values)

def load_json_file(filepath, connection):
    """Load events from a JSON file into database"""
    
    print(f'\nLoading file: {filepath}')
    
    # Read JSON file
    with open(filepath, 'r') as f:
        events = json.load(f)
    
    print(f'Found {len(events)} events in file')
    
    # Insert events
    cursor = connection.cursor()
    success_count = 0
    error_count = 0
    
    for idx, event in enumerate(events, 1):
        try:
            insert_event(cursor, event)
            success_count += 1
            
            if idx % 50 == 0:
                print(f'  Processed {idx}/{len(events)} events...')
        
        except Exception as e:
            error_count += 1
            print(f'  [ERROR] Failed to insert event {idx}: {e}')
    
    # Commit transaction
    connection.commit()
    
    print(f'\n[COMPLETE] Loaded {success_count} events successfully')
    if error_count > 0:
        print(f'[WARNING] {error_count} events failed to load')
    
    return success_count, error_count

def load_all_events(events_dir='data/events'):
    """Load all JSON files from events directory"""
    
    print('=' * 60)
    print('DATA LOADER - JSON to MySQL')
    print('=' * 60)
    
    # Connect to database
    connection = get_db_connection()
    if not connection:
        return
    
    # Find all JSON files
    json_files = [f for f in os.listdir(events_dir) if f.endswith('.json')]
    
    if not json_files:
        print(f'[WARNING] No JSON files found in {events_dir}')
        connection.close()
        return
    
    print(f'\nFound {len(json_files)} JSON file(s) to process')
    
    # Load each file
    total_success = 0
    total_errors = 0
    
    for json_file in json_files:
        filepath = os.path.join(events_dir, json_file)
        success, errors = load_json_file(filepath, connection)
        total_success += success
        total_errors += errors
    
    # Close connection
    connection.close()
    
    print('\n' + '=' * 60)
    print(f'[SUMMARY]')
    print(f'  Total events loaded: {total_success}')
    print(f'  Total errors: {total_errors}')
    print(f'  Files processed: {len(json_files)}')
    print('=' * 60)
    print('\nNext step: Query the data in MySQL Workbench!')

def main():
    """Main function"""
    load_all_events()

if __name__ == '__main__':
    main()