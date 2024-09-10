from pydantic import BaseModel
from datetime import date

class AutoBase(BaseModel):
    nombre: str
    precio: float
    fechaFabricacion: date
    activo: bool

class AutoCreate(AutoBase):
    pass

class AutoResponse(AutoBase):
    id: int

    class Config:
        orm_mode = True
