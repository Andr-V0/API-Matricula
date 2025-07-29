from fastapi import HTTPException, status
from models.pac import Pac
from utils.db import db
from bson import ObjectId

def create_new_pac(pac: Pac):
    try:
        existing_pac = db.pacs.find_one({"codigo": pac.codigo})
        if existing_pac:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este PAC ya existe")

        pac_dict = pac.dict()
        pac_dict["finalizar"] = False
        db.pacs.insert_one(pac_dict)
        return {"message": "PAC creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_all_pacs():
    try:
        pacs = []
        for pac in db.pacs.find():
            pac["_id"] = str(pac["_id"])
            pacs.append(pac)
        return pacs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_pac_by_codigo(codigo: str):
    try:
        pac = db.pacs.find_one({"codigo": codigo})
        if not pac:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PAC no encontrado")

        return {
            "_id": str(pac["_id"]),
            "codigo": pac["codigo"]
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def finalize_pac_by_codigo(codigo: str):
    try:
        pac = db.pacs.find_one({"codigo": codigo})
        if not pac:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PAC no encontrado")

        if pac.get("finalizar"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PAC ha finalizado")

        db.pac_anteriores.insert_one({
            "pac_id": pac["_id"],
            "codigo": pac["codigo"]
        })

        db.pacs.update_one(
            {"codigo": codigo},
            {"$set": {"finalizar": True}}
        )

        return {"message": "PAC finalizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def delete_pac_by_codigo(codigo: str):
    try:
        result = db.pacs.delete_one({"codigo": codigo})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PAC no encontrado")
        return {"message": "PAC borrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
