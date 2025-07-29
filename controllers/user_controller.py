from fastapi import HTTPException, status
from utils.db import db
from bson import ObjectId
from models.user_role import UserRoleUpdate

def update_user_role_by_id(user_id: str, role_update: UserRoleUpdate):
    try:
        # 1. Validar que el rol al que se quiere cambiar existe
        new_role_doc = db.tipos_usuarios.find_one({"codigo": role_update.role_code})
        if not new_role_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El rol con código '{role_update.role_code}' no existe."
            )

        # 2. Actualizar el campo tipoUsuario del usuario con el ObjectId del nuevo rol
        result = db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"tipoUsuario": new_role_doc["_id"]}}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El usuario con id '{user_id}' no fue encontrado."
            )

        return {"message": f"Rol del usuario {user_id} actualizado a {role_update.role_code} correctamente."}
    except Exception as e:
        # Capturar errores de conversión de ObjectId si el user_id es inválido
        if "is not a valid ObjectId" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El id de usuario '{user_id}' no es un ObjectId válido."
            )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
