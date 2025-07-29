from fastapi import APIRouter, Depends, status
from controllers.user_controller import update_user_role_by_id
from models.user_role import UserRoleUpdate
from utils.security import role_required

router = APIRouter()

@router.put("/users/{user_id}/role",
             dependencies=[Depends(role_required(["ADM"]))],
             summary="Update user role (Solo para Admins)",
             status_code=status.HTTP_200_OK)
def update_user_role(user_id: str, role_update: UserRoleUpdate):
    return update_user_role_by_id(user_id, role_update)
