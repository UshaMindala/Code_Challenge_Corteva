# app/ingestion.py
import os
import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models import Base, Station, WeatherRecord

# Configure basic logging so ingestion progress and issues
# are visible when running this script from the CLI or cron
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# """ functionality for below function """
#     Parse a single line from a raw weather data file.

#     Expected format (whitespace-separated): YYYYMMDD MAX MIN PRECIP

#     Values are typically stored in tenths of units and may include -9999 as a missing-value flag.

#     Returns:
#         (date, max_temp_c, min_temp_c, precip_cm)
#         or None if the line is malformed.
#     """
def parse_weather_line(line: str):
    parts = line.strip().split()
    if len(parts) != 4:
        return None
    raw_date, raw_max, raw_min, raw_precip = parts
    # convert date
    date = datetime.strptime(raw_date, "%Y%m%d").date()

# Convert temperature from tenths of °C to °C. Handles missing values encoded as -9999.
    def conv_temp(v):
        v = int(v)
        if v == -9999:
            return None
        return v / 10.0  # tenths of °C -> °C
    
# Convert precipitation from tenths of mm to cm. Handles missing values encoded as -9999.
    def conv_precip(v):
        v = int(v)
        if v == -9999:
            return None
        # tenths of mm -> mm -> cm
        mm = v / 10.0
        return mm / 10.0

    max_c = conv_temp(raw_max)
    min_c = conv_temp(raw_min)
    precip_cm = conv_precip(raw_precip)

    return date, max_c, min_c, precip_cm



# Fetch an existing station by code, or create it if it does not already exist.
# This ensures referential integrity before inserting weather records.
  
def get_or_create_station(db: Session, station_code: str):
    station = db.query(Station).filter_by(station_id=station_code).first()
    if station:
        return station
    station = Station(station_id=station_code)  # Create a new station record if not found
    db.add(station)
    db.commit()
    db.refresh(station)
    return station

# Ingest a single weather data file into the database.
# The station code is inferred from the filename.
# Returns: Number of successfully inserted weather records.

def ingest_file(db: Session, filepath: str) -> int:
    filename = os.path.basename(filepath)
    station_code, _ = os.path.splitext(filename) 
    station = get_or_create_station(db, station_code)

    count = 0
    with open(filepath, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parsed = parse_weather_line(line)
            if not parsed:
                continue
            date, max_c, min_c, precip_cm = parsed
            record = WeatherRecord(
                station_id=station.id,
                date=date,
                max_temp_c=max_c,
                min_temp_c=min_c,
                precip_cm=precip_cm,
            )
            db.add(record)
            try:
                db.commit()   # Commit per record so duplicates can be handled cleanly
                count += 1
            except IntegrityError:
                db.rollback()  # duplicate station + date, ignore
    return count



# Ingest all weather data files from a directory.
# This function:
# - Ensures database tables exist
# - Iterates over .txt files
# - Logs progress and totals
 
def ingest_all(wx_dir: str = "./wx_data"):
    Base.metadata.create_all(bind=engine)

    start = datetime.utcnow()
    logger.info("Starting ingestion from %s", wx_dir)

    db = SessionLocal()
    total = 0
    try:
        for fname in os.listdir(wx_dir):
            if not fname.endswith(".txt"):
                continue
            path = os.path.join(wx_dir, fname)
            logger.info("Ingesting file %s", path)
            n = ingest_file(db, path)
            logger.info("File %s: ingested %d records", path, n)
            total += n
    finally:
        db.close()
    end = datetime.utcnow()
    logger.info("Finished ingestion. Total records: %d. Start: %s End: %s", total, start, end)

if __name__ == "__main__":
    ingest_all()

