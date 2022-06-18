from pydantic import BaseModel

class CargoModel(BaseModel):
    Name: str
    CostPerHour: float

