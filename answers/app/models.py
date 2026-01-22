# app/models.py
from sqlalchemy import Column, Integer, String, Date, Float, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime, ForeignKey

Base = declarative_base()

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String(50), unique=True, index=True, nullable=False)
    state = Column(String(2), nullable=True)  # optional, from filename if you want ========================================
    name = Column(String(100), nullable=True)

    weather_records = relationship("WeatherRecord", back_populates="station")
    yearly_stats = relationship("WeatherYearlyStat", back_populates="station")


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    # data already converted to real units
    max_temp_c = Column(Float, nullable=True)
    min_temp_c = Column(Float, nullable=True)
    precip_cm = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    station = relationship("Station", back_populates="weather_records")

    __table_args__ = (
        UniqueConstraint("station_id", "date", name="uq_station_date"),
    )



class WeatherYearlyStat(Base):
    __tablename__ = "weather_yearly_stats"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)

    avg_max_temp_c = Column(Float, nullable=True)
    avg_min_temp_c = Column(Float, nullable=True)
    total_precip_cm = Column(Float, nullable=True)

    station = relationship("Station", back_populates="yearly_stats")

    __table_args__ = (
        UniqueConstraint("station_id", "year", name="uq_station_year"),
    )

