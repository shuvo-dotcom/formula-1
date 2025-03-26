from pydantic import BaseModel

class Team(BaseModel):
    name: str
    year_founded: int
    pole_positions: int
    race_wins: int
    constructor_titles: int
    previous_season_position: int
