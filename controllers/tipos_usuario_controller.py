from fastapi import HTTPException, status
from models.tipos_usuario import TiposUsuario
from utils.db import db
from bson import ObjectId

def create_new_tipo_usuario(tipo_usuario: TiposUsuario):
    try:
 
        if db.tipos_usuarios.find_one({"codigo": tipo_usuario.codigo}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de usuario con este codigo ya existe")

        db.tipos_usuarios.insert_one(tipo_usuario.dict())
        return {"message": "Tipo de usuario creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_all_tipos_usuario(codigo: str = None):
    try:
        if codigo:
            tipo_usuario = db.tipos_usuarios.find_one({"codigo": codigo})
            if not tipo_usuario:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tipo de usuario {codigo} no encontrado")
            usuarios = list(db.users.find({"tipoUsuario": str(tipo_usuario["_id"])}, {"nombre": 1, "email": 1, "_id": 0}))
            return usuarios
        else:
            tipos_usuario = list(db.tipos_usuarios.find())
            for tipo in tipos_usuario:
                tipo["_id"] = str(tipo["_id"])
            return tipos_usuario
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_tipo_usuario_by_id(id: str):
    try:
        tipo_usuario = db.tipos_usuarios.find_one({"_id": ObjectId(id)})
        if not tipo_usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de usuario no encontrado")
        tipo_usuario["_id"] = str(tipo_usuario["_id"])
        return tipo_usuario
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def update_tipo_usuario_by_id(id: str, tipo_usuario: TiposUsuario):
    try:
        result = db.tipos_usuarios.update_one({"_id": ObjectId(id)}, {"$set": tipo_usuario.dict()})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de usuario no encontrado")
        return {"message": "Tipo de usuario actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def delete_tipo_usuario_by_id(id: str):
    try:
        # Validar que no existan usuarios con este tipo
        if db.users.find_one({"tipoUsuario": ObjectId(id)}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puede borrar tipo de usuario con uno asociado")

        result = db.tipos_usuarios.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de usuario no encontrado")
        return {"message": "Tipo de usuario borrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
