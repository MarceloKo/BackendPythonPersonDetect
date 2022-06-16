from pydantic import BaseModel

class FuncionariosModel(BaseModel):
    Function: str 
    CostPerHour: float

