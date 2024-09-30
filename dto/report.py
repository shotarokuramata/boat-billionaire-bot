from dataclasses import dataclass
from dto.data import RaceDataDTO
from typing import Optional

@dataclass
class ReportDTO:
    def __init__(self, message: Optional[str] = None, race_url: Optional[str] = None,data: Optional[RaceDataDTO] = None):
        self.message = message
        self.race_url = race_url
        self.data = data


    def get_csv_header_list(self)->list[str]:
        data_list = self.data.get_field_list()
        append = ['race_url']
        return append + data_list

    def get_csv_body_list(self)->list:
        data_list = self.data.to_list()
        append = [self.race_url]
        return append + data_list
