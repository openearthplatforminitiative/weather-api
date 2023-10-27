from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Type(Enum):
    Feature = "Feature"


class SolarTime(BaseModel):
    time: str = Field(..., example="2019-12-03T13:52:13Z")


class Forecast(BaseModel):
    body: str
    sunrise: SolarTime
    sunset: SolarTime


class GeometryType(Enum):
    Point = "Point"


class PointGeometry(BaseModel):
    coordinates: List[float] = Field(..., example=[60.5, 11.59, 1001], min_items=2)
    type: GeometryType


class METJSONSunrise(BaseModel):
    copyright: str
    licenseURL: str
    type: Type = Field(..., example="Feature")
    geometry: PointGeometry
    properties: Forecast
