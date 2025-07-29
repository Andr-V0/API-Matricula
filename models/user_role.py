from pydantic import BaseModel

class UserRoleUpdate(BaseModel):
    role_code: str
