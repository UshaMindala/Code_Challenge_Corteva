# app/schemas.py
from datetime import date
from pydantic import BaseModel

#Shared schema for raw daily weather records.
class WeatherRecordBase(BaseModel):
    station_code: str                                       # Station identifier
    date: date                                              # Observation date
    max_temp_c: float | None = None                         # Daily maximum temperature in Celsius
    min_temp_c: float | None = None                         # Daily minimum temperature in Celsius
    precip_cm: float | None = None                          # Daily precipitation in centimeters

    class Config:
        orm_mode = True

#Shared schema for yearly aggregated weather statistics
class WeatherYearlyStatBase(BaseModel):
    station_code: str                                       # Station identifier
    year: int                                               # Calendar year for the aggregated statistics
    avg_max_temp_c: float | None = None                     # Average of daily max temperatures for the year
    avg_min_temp_c: float | None = None                     # Average of daily min temperatures for the year
    total_precip_cm: float | None = None                    # Total precipitation for the year

    class Config:
        orm_mode = True
