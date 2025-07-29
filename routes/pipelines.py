from fastapi import APIRouter, Depends, HTTPException, status, Query
from pipelines.matricula_pipelines import get_full_matricula_pipeline, get_asignaturas_stats_pipeline, lookup_pipeline
from utils.security import role_required

router = APIRouter()

@router.get("/matricula/full", dependencies=[Depends(role_required(["ADM"]))])
def get_full_matricula():
    try:
        return get_full_matricula_pipeline()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/asignaturas/stats", dependencies=[Depends(role_required("ADM"))])
def get_asignaturas_stats():
    try:
        return get_asignaturas_stats_pipeline()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/lookup", dependencies=[Depends(role_required(["ADM"]))])
def get_lookup(from_collection: str = Query(..., min_length=3, max_length=50),
                 local_field: str = Query(..., min_length=3, max_length=50),
                 foreign_field: str = Query(..., min_length=3, max_length=50),
                 as_field: str = Query(..., min_length=3, max_length=50)):
    try:
        return lookup_pipeline(from_collection, local_field, foreign_field, as_field)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
