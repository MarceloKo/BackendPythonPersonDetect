from pydantic import BaseModel,conlist

class QuartoModel(BaseModel):
    bedroom: int
    occupied: bool

