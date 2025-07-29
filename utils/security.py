from fastapi import Depends, HTTPException, status
from utils.auth_scheme import oauth2_scheme
from utils.jwt import verify_token
from typing import List

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

def role_required(required_roles: List[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker