from fastapi import HTTPException, status
from models.matricula import Matricula
from utils.db import db
from bson import ObjectId

def check_if_student_is_already_enrolled(student_id: str, pac_id: str):
    pipeline = [
        {
            "$match": {
                "usuarioId": student_id,
                "pacId": pac_id
            }
        },
        {
            "$count": "count"
        }
    ]
    result = list(db.matriculas.aggregate(pipeline))
    return len(result) > 0 and result[0]["count"] > 0

def create_new_matricula(matricula: Matricula, current_user: dict):
    try:
        # Validar que el pacId existe
        if not db.pac.find_one({"_id": ObjectId(matricula.pacId)}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid pacId")

        # Validar que el usuario que matricula es el autenticado
        db_user = db.users.find_one({"email": current_user.get("sub")})
        if str(db_user["_id"]) != matricula.usuarioId:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation no permitida")

        # Validar si el estudiante ya está matriculado en este PAC
        if check_if_student_is_already_enrolled(matricula.usuarioId, matricula.pacId):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El estudiante ya esta matricualdo en este PAC")

        # Validar que las clases existen y tienen cupos
        for clase in matricula.clases:
            asignatura = db.asignaturas.find_one({"_id": ObjectId(clase.claseId)})
            if not asignatura:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La asignatura con este id: {clase.claseId} no fue encontrada")
            if asignatura["cupos"] <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No hay cupos disponibles en {clase.claseId}")

        # Actualizar cupos
        for clase in matricula.clases:
            db.asignaturas.update_one({"_id": ObjectId(clase.claseId)}, {"$inc": {"cupos": -1}})

        db.matriculas.insert_one(matricula.dict())
        return {"message": "Matricula creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_all_matriculas(current_user: dict):
    try:
        if current_user.get("role") == "ADM":
            matriculas = list(db.matriculas.find())
        else:
            matriculas = list(db.matriculas.find({"usuarioId": current_user.get("sub")}))
        
        for matricula in matriculas:
            matricula["_id"] = str(matricula["_id"])
        return matriculas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def update_matricula_status_by_id(id: str, estado: str):
    try:
        result = db.matriculas.update_one({"_id": ObjectId(id)}, {"$set": {"estado": estado}})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matricula no encontrada")
        return {"message": "Matricula ha sido actualizada"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
