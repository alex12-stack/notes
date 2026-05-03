from fastapi import APIRouter

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import PatchMe

router = APIRouter(prefix="/users",tags=["Пользователи"])



@router.get("/me",response_model=PatchMe)
async def get_me(
        user_id: UserIdDep,
        db: DBDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user

@router.patch("/me")
async def edit_me(
        user_id: UserIdDep,
        db: DBDep,
        data: PatchMe,
):
    await db.users.edit(
        data=data.model_dump(exclude_unset=True),
        id=user_id,
    )
    user = db.users.get_one_or_none(id=user_id)
    return user