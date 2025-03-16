import enum

from sqlalchemy import Column, Integer, String

from database import Base


class StatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class Incident(Base):
    __tablename__ = "INCIDENT"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    actions_taken = Column(String, nullable=False)
    rca = Column(String, nullable=True)
    resolution = Column(String, nullable=True)
    status = Column(String, default=StatusEnum.OPEN)
