from fastapi import APIRouter, HTTPException

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import PatchMe, User

router = APIRouter(prefix="/users",tags=["Пользователи"])



@router.get("/me", response_model=User)
async def get_me(
        user_id: UserIdDep,
        db: DBDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.patch("/me", response_model=User)
async def edit_me(
        user_id: UserIdDep,
        db: DBDep,
        data: PatchMe,
):
    if not data.model_dump(exclude_unset=True):
        raise HTTPException(status_code=400, detail="Нет данных для обновления",)

    await db.users.edit(
        data=data,
        exclude_unset=True,
        id=user_id,
    )

    await db.commit()
    user = await db.users.get_one_or_none(id=user_id)
    return user