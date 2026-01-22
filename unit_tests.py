from app.database import SessionLocal
from app.models import Station, WeatherRecord

db = SessionLocal()

code = "USC00110072"

station = db.query(Station).filter(Station.station_id == code).first()
if station is None:
    print(f"Station {code} NOT found in stations table.")
else:
    print(f"Station {code} found with id={station.id}")
    count = db.query(WeatherRecord).filter(WeatherRecord.station_id == station.id).count()
    print(f"Weather records for {code}: {count}")

db.close()
