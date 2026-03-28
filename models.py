from pydantic import BaseModel
from typing import Dict, Optional

class Action(BaseModel):
    proposed_time: str
    duration: int
    decision: str
    message: str


class Observation(BaseModel):
    calendar: list
    request: dict
    preferences: dict
    history: list
    current_time: str


class Reward(BaseModel):
    score: float
    breakdown: Dict[str, float]
    explanation: Optional[str] = None