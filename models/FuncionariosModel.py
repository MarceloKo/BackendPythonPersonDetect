from pydantic import BaseModel

class FuncionariosModel(BaseModel):
    Name: str
    Function: str 
    CostPerHour: float

