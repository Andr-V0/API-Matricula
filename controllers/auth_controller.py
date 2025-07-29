from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from utils.firebase import create_firebase_user, get_firebase_user_by_email
from utils.db import db
from utils.jwt import create_access_token
from pymongo.errors import DuplicateKeyError

def create_new_user(user: User):
    try:

        if db.users.find_one({"cuenta": user.cuenta}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User con esta cuenta ya existe")

        if db.users.find_one({"nombre": user.nombre, "apellido": user.apellido}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User con este nombre y apellido ya existe")

        if user.email.endswith("@profesor.com"):
            tipo_usuario_codigo = "PROF"
        else:
            tipo_usuario_codigo = "EST"

        tipo_usuario = db.tipos_usuarios.find_one({"codigo": tipo_usuario_codigo})
        if not tipo_usuario:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Tipo de usuario {tipo_usuario_codigo} no encontrado")

        user_data = user.dict()
        user_data["tipoUsuario"] = tipo_usuario["_id"]

        firebase_user = create_firebase_user(user.email, user.password)
        user_data["firebase_uid"] = firebase_user.uid
        db.users.insert_one(user_data)
        return {"message": "User creado correctamente"}
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User con este email ya existe")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def login_for_access_token(form_data: OAuth2PasswordRequestForm):
    try:
        user = get_firebase_user_by_email(form_data.username)

        db_user = db.users.find_one({"email": form_data.username})
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User no encontrado")
 
        # Buscar el documento del tipo de usuario para obtener el código del rol
        tipo_usuario_doc = db.tipos_usuarios.find_one({"_id": db_user["tipoUsuario"]})
        if not tipo_usuario_doc:
            raise HTTPException(status_code=500, detail="Inconsistencia de datos: el rol del usuario no fue encontrado.")

        role_code = tipo_usuario_doc["codigo"]
        access_token = create_access_token(data={"sub": db_user["email"], "role": role_code})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_user_profile(current_user: dict):
    try:
        # El email del usuario está en el campo 'sub' del token JWT
        user_email = current_user.get("sub")
        db_user = db.users.find_one(
            {"email": user_email},
            {"nombre": 1, "apellido": 1, "email": 1, "_id": 0}  # Proyección para no devolver datos sensibles
        )
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User no encontrado")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
