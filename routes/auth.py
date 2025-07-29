from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from controllers.auth_controller import create_new_user, login_for_access_token, get_user_profile
from utils.security import get_current_user
from utils.auth_scheme import oauth2_scheme

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    return create_new_user(user)

@router.post("/login",
             summary="Login User",
             description="""

- **username**: Aqui es el **email** del usuario.
- **password**: La contraseña del mismo.

""")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_for_access_token(form_data)

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return get_user_profile(current_user)
