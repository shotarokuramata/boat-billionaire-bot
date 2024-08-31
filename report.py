from dataclasses import dataclass
from data import RaceDataDTO
from typing import Optional

@dataclass
class ReportDTO:
    def __init__(self, message: Optional[str] = None, race_url: Optional[str] = None,data: Optional[RaceDataDTO] = None):
        self.message = message
        self.race_url = race_url
        self.data = data
