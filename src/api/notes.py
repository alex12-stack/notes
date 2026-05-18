from fastapi import APIRouter,Depends,HTTPException

from src.api.dependencies import PaginationDep
from src.api.dependencies import DBDep
from src.api.dependencies import UserIdDep
from src.schemas.notes import GetNotesFiltered, CreateNote, CreateNoteDB, PatchNote, Note

router = APIRouter(prefix="/notes",tags=["Заметки"])



@router.get("", response_model=list[Note])
async def get_notes(
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
        offset=per_page*(pagination.page-1),
    )
    return res



@router.post("", response_model=Note)
async def post_notes(
        user_id: UserIdDep,
        db: DBDep,
        params: CreateNote,
):
    res = await db.notes.add(
        CreateNoteDB(
            **params.model_dump(),
            owner_id=user_id,
        )
    )
    await db.commit()
    return res



@router.patch("/{note_id}")
async def put_note(
        note_id: int,
        user_id: UserIdDep,
        db: DBDep,
        params: PatchNote,
):
    if not params.model_dump(exclude_unset=True):
        raise HTTPException(status_code=400, detail="Нет данных для обновления")

    if params.folder_id is not None:
        folder = await db.folders.get_one_or_none(id=params.folder_id, owner_id=user_id)
        if not folder:
            raise HTTPException(status_code=404, detail="Папка не найдена или нет доступа")

    res = await db.notes.edit(
        data=params,
        exclude_unset=True,
        id=note_id,
        owner_id=user_id,
    )
    if res == 0:
        raise HTTPException(status_code=404, detail="Заметка не найдена или нет доступа")
    await db.commit()
    return {"status": "updated"}


@router.delete("/{note_id}")
async def delete_note(
        note_id: int,
        user_id: UserIdDep,
        db: DBDep,
):
    res = await db.notes.delete(id=note_id, owner_id=user_id)
    if res == 0:
        raise HTTPException(status_code=404,detail="Заметка не найдена или нет доступа")
    await db.commit()
    return {"status": "deleted"}