from pydantic import BaseModel
from typing import Optional

class Pac(BaseModel):
    id: Optional[str] = None
    codigo: str
    finalizar: bool = False
