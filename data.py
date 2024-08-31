from dataclasses import dataclass

@dataclass
class RaceDataDTO:
    escape_last_year: float = 0
    escape_last_half_year: float = 0
    allow_escape_last_year: float = 0
    allow_escape_last_half_year: float = 0
    pierce_last_year: float = 0
    overtake_last_year: float = 0
    first_place_in_last_ten_race: int = 0

    def is_target(self)->bool:
        return (
            self.escape_last_year >= 60 and
            self.escape_last_half_year >= 55 and
            self.allow_escape_last_year >= 60 and
            self.allow_escape_last_half_year >= 60 and
            self.pierce_last_year < 11.0 and
            self.overtake_last_year < 22.0 and
            self.first_place_in_last_ten_race >= 6
        )
