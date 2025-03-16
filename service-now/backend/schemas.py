from enum import Enum
from typing import Optional

from pydantic import BaseModel


class StatusEnum(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class IncidentBase(BaseModel):
    description: str
    actions_taken: str


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    rca: Optional[str] = None
    resolution: Optional[str] = None
    status: Optional[StatusEnum] = None


class Incident(IncidentBase):
    id: int
    rca: Optional[str] = None
    resolution: Optional[str] = None
    status: StatusEnum

    class Config:
        from_attributes = True
