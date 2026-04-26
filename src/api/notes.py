from fastapi import APIRouter,Depends,HTTPException

from src.api.dependencies import PaginationDep
from src.api.dependencies import DBDep
from src.api.dependencies import UserIdDep
from src.schemas.notes import GetNotesFiltered, CreateNote, PatchNote

router = APIRouter(prefix="/notes",tags=["Заметки"])



@router.get("")
async def get_notes(
        pagination:PaginationDep,
        db: DBDep,
        user_id: UserIdDep,
):
    per_page = pagination.per_page or 5
    res = await db.notes.get_all(
        owner_id=user_id,
        limit=per_page,
        offset=per_page*(pagination.page-1)
    )
    return res



@router.get("/search")
async def search_notes(
        pagination:PaginationDep,
        db: DBDep,
        user_id: UserIdDep,
        filters: GetNotesFiltered = Depends(),
):
    per_page = pagination.per_page or 5
    res = await db.notes.get_all(
        owner_id=user_id,
        **filters.model_dump(exclude_none=True),
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )
    return res



@router.post("")
async def post_notes(
        user_id: UserIdDep,
        db: DBDep,
        params: CreateNote,
):
    res = await db.notes.add({**params.model_dump(),"owner_id":user_id})
    return res



@router.patch("/{note_id}")
async def put_note(
        note_id: int,
        user_id: UserIdDep,
        db: DBDep,
        params: PatchNote,
):
    res = await db.notes.edit(
        data=params.model_dump(exclude_unset=True),
        id=note_id,
        owner_id=user_id
    )
    return res


@router.delete("/{note_id}")
async def delete_note(
        note_id: int,
        user_id: UserIdDep,
        db: DBDep,
):
    res = await db.notes.delete(note_id=note_id,owner_id=user_id)
    if res == 0:
        raise HTTPException(status_code=404,detail="Заметка не найдена или нет доступа")
    return {"status": "deleted"}