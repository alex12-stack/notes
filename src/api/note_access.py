from fastapi import APIRouter, Query, HTTPException

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.note_access import AddRole, AddRoleDB, Role


router = APIRouter(prefix="/note_access",tags=["Доступ к заметкам"])


@router.get("/{note_id}")
async def get_access_by_role(
        note_id: int,
        user_id: UserIdDep,
        db: DBDep,
        role: Role | None = Query(default=None),
):
    note = await db.notes.get_one_or_none(id=note_id)
    if not note:
        raise HTTPException(status_code=404,detail="такой заметки нет")
    if note.owner_id != user_id:
        raise HTTPException(status_code=403,detail="эта заметка принадлежит не вам")

    if role:
        res = await db.note_access.get_all(note_id=note_id, role=role)
    else:
        res = await db.note_access.get_all(note_id=note_id)

    return [user.user_id for user in res]


@router.post("/{note_id}")
async def add_role(
        note_id: int,
        cur_user_id: UserIdDep,
        db: DBDep,
        data: AddRole,
):
    note = await db.notes.get_one_or_none(id=note_id,owner_id=cur_user_id)
    if not note:
        raise HTTPException(status_code=404,detail="такой заметки нет или она не ваша")

    user = await db.users.get_one_or_none(id=data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="такого пользователя нет")

    await db.note_access.add(
        AddRoleDB(
            note_id=note_id,
            user_id=data.user_id,
            role=data.role,
        )
    )

    await db.commit()
    return {"status": "created"}


@router.delete("/{note_id}/{user_id}")
async def delete_role(
        note_id: int,
        user_id: int,
        cur_user_id: UserIdDep,
        db: DBDep,
):
    note = await db.notes.get_one_or_none(id=note_id, owner_id=cur_user_id)
    if not note:
        raise HTTPException(status_code=404,detail="такой заметки нет или она не ваша")
    res = await db.note_access.delete(
        note_id=note_id,
        user_id=user_id,
    )
    if res == 0:
        raise HTTPException(status_code=404,detail="У пользователя нет доступа")

    await db.commit()
    return {"status": "deleted"}
