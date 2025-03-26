from pydantic import BaseModel

class Driver(BaseModel):
    name: str
    age: int
    team: str
    pole_positions: int
    race_wins: int
    points_scored: int
    world_titles: int
    fastest_laps: int
