# app/schemas.py
from datetime import date
from pydantic import BaseModel

class WeatherRecordBase(BaseModel):
    station_code: str
    date: date
    max_temp_c: float | None = None
    min_temp_c: float | None = None
    precip_cm: float | None = None

    class Config:
        orm_mode = True


class WeatherYearlyStatBase(BaseModel):
    station_code: str
    year: int
    avg_max_temp_c: float | None = None
    avg_min_temp_c: float | None = None
    total_precip_cm: float | None = None

    class Config:
        orm_mode = True
