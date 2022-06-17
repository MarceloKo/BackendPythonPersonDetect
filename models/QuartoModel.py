from pydantic import BaseModel

class QuartoModel(BaseModel):
    bedroom: int
    occupied: bool

