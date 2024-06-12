from pydantic import BaseModel

class ParticipantBase(BaseModel):
    name: str
    age: int
    score: float

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int

    class Config:
        orm_mode = True
