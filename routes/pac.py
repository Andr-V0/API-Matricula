from fastapi import APIRouter, Depends
from models.pac import Pac
from controllers.pac_controller import (
    create_new_pac,
    get_all_pacs,
    get_pac_by_codigo,
    finalize_pac_by_codigo,
    delete_pac_by_codigo,
)
from utils.security import role_required

router = APIRouter(prefix="/pac", dependencies=[Depends(role_required(["ADM"]))])


@router.post("/")
async def create_pac(pac: Pac):
    return create_new_pac(pac)


@router.get("/")
async def get_pacs():
    return get_all_pacs()


@router.get("/{codigo}")
async def get_pac(codigo: str):
    return get_pac_by_codigo(codigo)


@router.put("/{codigo}/finalize")
async def finalize_pac(codigo: str):
    return finalize_pac_by_codigo(codigo)


@router.delete("/{codigo}")
async def delete_pac(codigo: str):
    return delete_pac_by_codigo(codigo)