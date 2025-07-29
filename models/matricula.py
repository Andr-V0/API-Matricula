from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Clase(BaseModel):
    claseId: str
    estado: str

class Matricula(BaseModel):
    id: Optional[str] = None
    usuarioId: str
    pacId: str
    fecha: datetime = Field(default_factory=datetime.now)
    clases: List[Clase]
    estado: str
