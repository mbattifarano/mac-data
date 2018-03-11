"""Weather Underground Models

Defines SQLAlchemy data models for the weather underground API
"""
from mac_data.orm import Base
from sqlalchemy import Column, Integer, DateTime, Float, String


class WeatherUndergroundObservation(Base):
    __tablename__ ='weather_underground_observations'

    id = Column(Integer, primary_key=True)
    zipcode = Column(String, index=True)
    recorded_at = Column(DateTime(timezone=True), index=True)
    temperature = Column(Float)
    dew_point = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_gust = Column(Float)
    visibility = Column(Float)
    pressure = Column(Float)
    windchill = Column(Float)
    heat_index = Column(Float)
    precipitation = Column(Float)
    fog = Column(Float)
    rain = Column(Float)
    snow = Column(Float)
    condition = Column(String)
