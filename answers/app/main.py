# app/main.py
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from .database import SessionLocal, engine
from .models import Base, WeatherRecord, Station, WeatherYearlyStat
from .schemas import WeatherRecordBase, WeatherYearlyStatBase

Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(title="Weather API", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------------------------------
#   Weather records endpoint
# -------------------------------------------------------

# Return raw daily weather records with optional filters.
#     Supports filtering by:
#     - station_id
#     - date range (date_from, date_to)
#Includes pagination via offset and limit.

@app.get("/api/weather", response_model=List[WeatherRecordBase])
def get_weather(
    station_id: Optional[str] = Query(None, description="Station code"),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    q = (
        db.query(WeatherRecord, Station.station_id.label("station_code"))
        .join(Station, WeatherRecord.station_id == Station.id)
    )

    if station_id:
        q = q.filter(Station.station_id == station_id)

    if date_from:
        q = q.filter(WeatherRecord.date >= date_from)
    if date_to:
        q = q.filter(WeatherRecord.date <= date_to)

    q = q.order_by(WeatherRecord.date).offset(offset).limit(limit)
    rows = q.all()

    # map rows into schema
    result = []
    for wr, station_code in rows:
        result.append(
            WeatherRecordBase(
                station_code=station_code,
                date=wr.date,
                max_temp_c=wr.max_temp_c,
                min_temp_c=wr.min_temp_c,
                precip_cm=wr.precip_cm,
            )
        )
    return result

# -------------------------------------------------------
#   Yearly weather statistics endpoint
# -------------------------------------------------------

# Return yearly aggregated weather statistics.
# Supports filtering by:
# - station_id
# - year
# Includes pagination for large result sets.

@app.get("/api/weather/stats", response_model=List[WeatherYearlyStatBase])
def get_weather_stats(
    station_id: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    q = (
        db.query(WeatherYearlyStat, Station.station_id.label("station_code"))
        .join(Station, WeatherYearlyStat.station_id == Station.id)
    )
    if station_id:
        q = q.filter(Station.station_id == station_id)
    if year:
        q = q.filter(WeatherYearlyStat.year == year)

    q = q.order_by(WeatherYearlyStat.year).offset(offset).limit(limit)
    rows = q.all()

    result = []
    for stat, station_code in rows:
        result.append(
            WeatherYearlyStatBase(
                station_code=station_code,
                year=stat.year,
                avg_max_temp_c=stat.avg_max_temp_c,
                avg_min_temp_c=stat.avg_min_temp_c,
                total_precip_cm=stat.total_precip_cm,
            )
        )
    return result
