from dataclasses import dataclass, fields
import json

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
        with open('config_race_data.json', 'r') as f:
            json_data = json.load(f)

        return (
            (json_data.get('escape_last_year', 0) == 0 or self.escape_last_year >= json_data['escape_last_year']) and
            (json_data.get('escape_last_half_year', 0) == 0 or self.escape_last_half_year >= json_data['escape_last_half_year']) and
            (json_data.get('allow_escape_last_year', 0) == 0 or self.allow_escape_last_year >= json_data['allow_escape_last_year']) and
            (json_data.get('allow_escape_last_half_year', 0) == 0 or self.allow_escape_last_half_year >= json_data['allow_escape_last_half_year']) and
            (json_data.get('pierce_last_year', 0) == 0 or self.pierce_last_year < json_data['pierce_last_year']) and
            (json_data.get('overtake_last_year', 0) == 0 or self.overtake_last_year < json_data['overtake_last_year']) and
            (json_data.get('first_place_in_last_ten_race', 0) == 0 or self.first_place_in_last_ten_race >= json_data['first_place_in_last_ten_race'])
        )

    def to_list(self)->list[float|int]:
        return [
            self.escape_last_year,
            self.escape_last_half_year,
            self.allow_escape_last_year,
            self.allow_escape_last_half_year,
            self.pierce_last_year,
            self.overtake_last_year,
            self.first_place_in_last_ten_race
        ]

    def get_field_list(self)->list[str]:
        return [field.name for field in fields(self)]
