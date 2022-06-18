from datetime import datetime
from pydantic import BaseModel

class Quartofluxomodel(BaseModel):
    idQuarto: str
    idQuartoFluxoStatus: str
