# app/analysis.py
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, WeatherRecord, WeatherYearlyStat

def compute_yearly_stats():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # group by station, year
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

        for r in rows:
            year = int(r.year)
            stat = (
                db.query(WeatherYearlyStat)
                .filter_by(station_id=r.station_id, year=year)
                .first()
            )
            if not stat:
                stat = WeatherYearlyStat(
                    station_id=r.station_id,
                    year=year,
                )

            stat.avg_max_temp_c = float(r.avg_max) if r.avg_max is not None else None
            stat.avg_min_temp_c = float(r.avg_min) if r.avg_min is not None else None
            stat.total_precip_cm = float(r.sum_precip) if r.sum_precip is not None else None

            db.add(stat)

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    compute_yearly_stats()
