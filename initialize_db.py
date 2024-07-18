import psycopg2
from dotenv import load_dotenv
import os

def initialize_db():
    conn = psycopg2.connect(
        database=os.getenv('DATABSE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASS'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT')
    )
    c = conn.cursor()
    # Create the events table
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            base_event_id INTEGER PRIMARY KEY,
            event_id INTEGER,
            title TEXT,
            event_start_date TIMESTAMP,
            event_end_date TIMESTAMP,
            sell_from TIMESTAMP,
            sell_to TIMESTAMP,
            sold_out BOOLEAN,
            sell_mode TEXT
        )
    ''')
    
    # Create the zones table
    c.execute('''
        CREATE TABLE IF NOT EXISTS zones (
            id SERIAL PRIMARY KEY,
            base_event_id INTEGER,
            zone_id INTEGER,
            capacity INTEGER,
            price NUMERIC,
            name TEXT,
            numbered BOOLEAN,
            FOREIGN KEY (base_event_id) REFERENCES events(base_event_id) ON DELETE CASCADE
        )
    ''')
    
    # Create the index on event_start_date and event_end_date
    c.execute('''
        CREATE INDEX IF NOT EXISTS idx_event_date
        ON events (event_start_date, event_end_date)
    ''')
    
    # Cluster the table based on the idx_event_date index
    c.execute('''
        CLUSTER events USING idx_event_date
    ''')
    
    # Optionally, set the table to auto-vacuum analyze to keep stats updated
    c.execute('''
        ALTER TABLE events SET (autovacuum_analyze_scale_factor = 0.01);
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Initialize the database
    load_dotenv()
    initialize_db()