# app/analysis.py

# SQLAlchemy utilities for SQL functions and date extraction
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

# Database session factory and engine
from database import SessionLocal, engine

# ORM models for raw weather data and yearly summary stats
from models import Base, WeatherRecord, WeatherYearlyStat


# """ Requirement """
# Compute yearly aggregated weather statistics for each station
# and store/update results in the WeatherYearlyStat table.

# This "compute_yearly_stats" function:
# - Ensures required tables exist
# - Aggregates raw daily records into yearly summaries
# - Upserts (insert or update) yearly statistics per station
# """
def compute_yearly_stats():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # -------------------------------
        # Step 1: Aggregate raw weather data
        # -------------------------------
        # Group by station_id and year extracted from the date column.
        # Compute: Average max temperature , Average min temperature , Total precipitation

        rows = (
            db.query(
                WeatherRecord.station_id.label("station_id"),
                extract("year", WeatherRecord.date).label("year"),
                func.avg(WeatherRecord.max_temp_c).label("avg_max"),
                func.avg(WeatherRecord.min_temp_c).label("avg_min"),
                func.sum(WeatherRecord.precip_cm).label("sum_precip"),
            )
            .group_by(WeatherRecord.station_id, extract("year", WeatherRecord.date))
            .all()
        )

        # -------------------------------
        # Step 2: Upsert yearly stats
        # -------------------------------
        # Loop through each aggregated result and
        # insert or update the yearly stats (WeatherYearlyStat) table

        for r in rows:
            year = int(r.year)
            # Check if a yearly stat record already exists for this station and year
            stat = (
                db.query(WeatherYearlyStat)
                .filter_by(station_id=r.station_id, year=year)
                .first()
            )

            # If no existing record, create a new one
            if not stat:
                stat = WeatherYearlyStat(
                    station_id=r.station_id,
                    year=year,
                )

            # -------------------------------
            # Step 3: Populate aggregated fields and handle NULLs explicitly
            # -------------------------------

            stat.avg_max_temp_c = float(r.avg_max) if r.avg_max is not None else None
            stat.avg_min_temp_c = float(r.avg_min) if r.avg_min is not None else None
            stat.total_precip_cm = float(r.sum_precip) if r.sum_precip is not None else None

            db.add(stat)
        # Commit all the changes
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    compute_yearly_stats()
