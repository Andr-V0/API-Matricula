from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    
    nombre: str
    apellido: str
    cuenta: str
    email: EmailStr
    password: str
    
    fechaAlta: datetime = datetime.now()
