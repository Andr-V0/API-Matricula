from fastapi import HTTPException, status
from models.asignatura import Asignatura
from utils.db import db
from bson import ObjectId
from typing import Optional

def create_new_asignatura(asignatura: Asignatura):
    try:

        if db.asignaturas.find_one({"seccion": asignatura.seccion, "nombre": asignatura.nombre}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta asignatura ya existe")

        # Validar que el pacId existe
        if not db.pac.find_one({"_id": ObjectId(asignatura.pacId)}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid pacId")

        db.asignaturas.insert_one(asignatura.dict())
        return {"message": "Asignatura creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_all_asignaturas():
    try:
        asignaturas = list(db.asignaturas.find())
        for asignatura in asignaturas:
            asignatura["_id"] = str(asignatura["_id"])
        return asignaturas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def search_all_asignaturas(nombre: Optional[str]):
    try:
        query = {}
        if nombre:
            query["nombre"] = {"$regex": nombre, "$options": "i"}

        asignaturas = list(db.asignaturas.find(query))
        for asignatura in asignaturas:
            asignatura["_id"] = str(asignatura["_id"])
        return asignaturas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_asignatura_by_id(id: str):
    try:
        asignatura = db.asignaturas.find_one({"_id": ObjectId(id)})
        if not asignatura:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no encontrada")
        asignatura["_id"] = str(asignatura["_id"])
        return asignatura
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def update_asignatura_by_id(id: str, asignatura: Asignatura):
    try:
        result = db.asignaturas.update_one({"_id": ObjectId(id)}, {"$set": asignatura.dict()})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no econtrada")
        return {"message": "Asignatura actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def delete_asignatura_by_id(id: str):
    try:
        # Validar que no existan matriculas ya asociadas a esta asignatura
        if db.matriculas.find_one({"clases.claseId": id}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puede borrar asignaturas con matriculas asociadas")

        result = db.asignaturas.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no encontrada")
        return {"message": "Asignatura borrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
