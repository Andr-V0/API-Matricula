from fastapi import APIRouter, Depends, status
from models.matricula import Matricula
from utils.security import role_required, get_current_user
from controllers.matricula_controller import (
    create_new_matricula,
    get_all_matriculas,
    update_matricula_status_by_id,
)

router = APIRouter()

@router.post("/matricula", dependencies=[Depends(role_required(["EST"]))], status_code=status.HTTP_201_CREATED)
def create_matricula(matricula: Matricula, current_user: dict = Depends(get_current_user)):
    return create_new_matricula(matricula, current_user)

@router.get("/matricula")
def get_matriculas(current_user: dict = Depends(get_current_user)):
    return get_all_matriculas(current_user)

@router.put("/matricula/{id}", dependencies=[Depends(role_required("ADM"))])
def update_matricula_status(id: str, estado: str):
    return update_matricula_status_by_id(id, estado)