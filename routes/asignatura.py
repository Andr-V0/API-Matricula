from fastapi import APIRouter, Depends, status, Query
from models.asignatura import Asignatura
from utils.security import role_required, get_current_user
from typing import Optional
from controllers.asignatura_controller import (
    create_new_asignatura,
    get_all_asignaturas,
    search_all_asignaturas,
    get_asignatura_by_id,
    update_asignatura_by_id,
    delete_asignatura_by_id,
)

router = APIRouter()

@router.post("/asignaturas", dependencies=[Depends(role_required(["PROF"]))], status_code=status.HTTP_201_CREATED)
def create_asignatura(asignatura: Asignatura):
    return create_new_asignatura(asignatura)

@router.get("/asignaturas")
def get_asignaturas():
    return get_all_asignaturas()

@router.get("/asignaturas/search")
def search_asignaturas(nombre: Optional[str] = Query(None, min_length=3, max_length=50)):
    return search_all_asignaturas(nombre)

@router.get("/asignaturas/{id}")
def get_asignatura(id: str):
    return get_asignatura_by_id(id)

@router.put("/asignaturas/{id}", dependencies=[Depends(role_required("PROF"))])
def update_asignatura(id: str, asignatura: Asignatura):
    return update_asignatura_by_id(id, asignatura)

@router.delete("/asignaturas/{id}", dependencies=[Depends(role_required("PROF"))])
def delete_asignatura(id: str):
    return delete_asignatura_by_id(id)