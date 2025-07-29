from utils.db import db
from bson import ObjectId

def get_full_matricula_pipeline():
    pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "usuarioId",
                "foreignField": "_id",
                "as": "usuario"
            }
        },
        {
            "$unwind": "$usuario"
        },
        {
            "$lookup": {
                "from": "pac",
                "localField": "pacId",
                "foreignField": "_id",
                "as": "pac"
            }
        },
        {
            "$unwind": "$pac"
        },
        {
            "$project": {
                "_id": 0,
                "usuario": "$usuario.nombre",
                "pac": "$pac.codigo",
                "fecha": 1,
                "estado": 1,
                "clases": 1
            }
        }
    ]
    return list(db.matriculas.aggregate(pipeline))

def get_asignaturas_stats_pipeline():
    pipeline = [
        {
            "$unwind": "$clases"
        },
        {
            "$group": {
                "_id": "$clases.claseId",
                "count": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from": "asignaturas",
                "localField": "_id",
                "foreignField": "_id",
                "as": "asignatura"
            }
        },
        {
            "$unwind": "$asignatura"
        },
        {
            "$project": {
                "_id": 0,
                "asignatura": "$asignatura.nombre",
                "matriculados": "$count"
            }
        }
    ]
    return list(db.matriculas.aggregate(pipeline))

def lookup_pipeline(from_collection: str, local_field: str, foreign_field: str, as_field: str):
    pipeline = [
        {
            "$lookup": {
                "from": from_collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_field
            }
        }
    ]
    return list(db.matriculas.aggregate(pipeline))
