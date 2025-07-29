from pydantic import BaseModel
from typing import Optional

class TiposUsuario(BaseModel):
    id: Optional[str] = None
    codigo: str
