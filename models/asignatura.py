from pydantic import BaseModel
from typing import Optional

class Asignatura(BaseModel):
    id: Optional[str] = None
    seccion: str
    nombre: str
    cupos: int
    pacId: str
