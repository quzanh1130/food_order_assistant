import os
from dotenv import load_dotenv

os.environ['RUN_TIMEZONE_CHECK'] = '0'

from database.db import init_db
from database.ingest import ingest_data

load_dotenv()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    ingest_data()
    print("Database initialized")