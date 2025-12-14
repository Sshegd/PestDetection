from pydantic import BaseModel
from typing import Optional

class ScanRequest(BaseModel):
    district: str
    soilType: str
    primaryCrop: str
    secondaryCrop: Optional[str] = None
    language: str = "en"


class PestAlert(BaseModel):
    crop: str
    pest: str
    risk: str
    symptoms: str
    preventive: str
    treatment: str


class PestResponse(BaseModel):
    alerts: list[PestAlert]
