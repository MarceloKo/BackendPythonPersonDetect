from pydantic import BaseModel

class Fluxosdehorasmodel(BaseModel):
    RoomNumber: str
    Employees: list
    EntryTime: str 
    ExitTime: str
    Date: str
    TotalCostForTheRoom: float

