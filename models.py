from pydantic import BaseModel
from typing import List

class ScanRequest(BaseModel):
    district: str
    soilType: str
    language: str = "en"


class PestAlert(BaseModel):
    cropName: str
    pestName: str
    riskLevel: str
    symptoms: List[str]
    preventive: List[str]
    corrective: List[str]


class PestResponse(BaseModel):
    alerts: List[PestAlert]

