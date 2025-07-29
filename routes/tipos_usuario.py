from fastapi import APIRouter, Depends, status
from models.tipos_usuario import TiposUsuario
from utils.security import role_required
from controllers.tipos_usuario_controller import (
    create_new_tipo_usuario,
    get_all_tipos_usuario,
    get_tipo_usuario_by_id,
    update_tipo_usuario_by_id,
    delete_tipo_usuario_by_id,
)

router = APIRouter()

@router.post("/tipos_usuario", dependencies=[Depends(role_required(["ADM"]))], status_code=status.HTTP_201_CREATED)
def create_tipo_usuario(tipo_usuario: TiposUsuario):
    return create_new_tipo_usuario(tipo_usuario)

@router.get("/tipos_usuario", dependencies=[Depends(role_required(["ADM"]))])
def get_tipos_usuario(codigo: str = None):
    return get_all_tipos_usuario(codigo)

@router.get("/tipos_usuario/{id}", dependencies=[Depends(role_required(["ADM"]))])
def get_tipo_usuario(id: str):
    return get_tipo_usuario_by_id(id)

@router.put("/tipos_usuario/{id}", dependencies=[Depends(role_required(["ADM"]))])
def update_tipo_usuario(id: str, tipo_usuario: TiposUsuario):
    return update_tipo_usuario_by_id(id, tipo_usuario)

@router.delete("/tipos_usuario/{id}", dependencies=[Depends(role_required(["ADM"]))])
def delete_tipo_usuario(id: str):
    return delete_tipo_usuario_by_id(id)