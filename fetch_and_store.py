import requests
from xml.etree import ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv
import logging
import os
import psycopg2
import schedule
import time
import threading

def fetch_events(api_url: str = ''):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"An error occurred while fetch data from api {e}")

    all_events = ET.fromstring(response.content).findall('.//base_event')
    return all_events


def get_database_connection():
    conn = psycopg2.connect(
        database=os.getenv('DATABSE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASS'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT')
    )

    return conn

def store_data_in_db(base_event, event):
    
    # Establish a connection to the PostgreSQL database
    connection = get_database_connection()

    with connection as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT 1 FROM events WHERE base_event_id = %s", (base_event.get('base_event_id'),))
        
        if cur.fetchone():
            
             # Update the event if it already exists
            cur.execute("UPDATE events SET event_id = %s, title = %s, event_start_date = %s, event_end_date = %s, sell_from = %s, sell_to = %s, sold_out = %s, sell_mode = %s WHERE base_event_id = %s",
                        (event.get('event_id'), base_event.get('title'), datetime.fromisoformat(event.get('event_start_date')), datetime.fromisoformat(event.get('event_end_date')), datetime.fromisoformat(event.get('sell_from')), datetime.fromisoformat(event.get('sell_to')), event.get('sold_out') == 'true', base_event.get('sell_mode'), base_event.get('base_event_id')))
         
        else:
            # Insert the API data into the table
            cur.execute("INSERT INTO events (base_event_id, event_id, title, event_start_date, event_end_date, sell_from, sell_to, sold_out, sell_mode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (base_event.get('base_event_id'), event.get('event_id'), base_event.get('title'), datetime.fromisoformat(event.get('event_start_date')), \
                     datetime.fromisoformat(event.get('event_end_date')), datetime.fromisoformat(event.get('sell_from')), \
                          datetime.fromisoformat(event.get('sell_to')), event.get('sold_out') == 'true', base_event.get('sell_mode')))
        
        
        # Delete existing zones for the event
        cur.execute("DELETE FROM zones WHERE base_event_id = %s", (base_event.get('base_event_id'),))

        for zone in event.findall('zone'):
            cur.execute("INSERT INTO zones (zone_id, base_event_id, capacity, price, name, numbered) VALUES (%s, %s, %s, %s, %s, %s)",
                    (zone.get('zone_id'), base_event.get('base_event_id'), zone.get('capacity'), \
                     zone.get('price'), zone.get('name'), zone.get('numbered') == 'true'))
            
        conn.commit()
        cur.close()
    

if __name__ == '__main__':
    # Load the environment variables from.env file
    load_dotenv()

    # Fetch the events
    api_url = os.getenv('PROVIDER_API')
    
    events = fetch_events(api_url)
    
    for base_event in events:
        for event in base_event.findall('event'):
            try:
                sell_mode = base_event.get('sell_mode')
                # Check and filter out only those events which are 'online' and lies between given range
                if sell_mode == 'online':
                    store_data_in_db(base_event=base_event, event=event)
            except Exception as ex:
                logging.error(f'An error occurred in processing and storing the data in db {ex}')