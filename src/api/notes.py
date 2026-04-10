from fastapi import Query, APIRouter

from sqlalchemy import Enum

from src.schemas.notes import Note, NotePatch

from src.repositories.notes import NotesRepository
from src.api.dependencies import PaginationDep
from src.db import async_session_maker

import datetime

import enum

class Is_Public(enum.Enum):
    Public="public"
    Private="private"

router = APIRouter(prefix="/notes")

@router.get("")
async def get_notes(
        pagination:PaginationDep,
        content: str,
        title: str = Query(default="New note"),
        is_public: Is_Public = Query(default=Is_Public.Private),
        folder_id: int | None = Query(default=None),
        created_at: datetime.datetime = Query(default=datetime.datetime.now()),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await NotesRepository(session).get_all(
            content=content,
            title=title,
            folder_id=folder_id,
            is_public=is_public,
            created_at=created_at,
            limit=per_page,
            offset=per_page*(pagination.page-1)
        )

@router.post("")
async def create_note(note:Note):
    async with async_session_maker() as session:
        new_folder = await NotesRepository(session).add(note)
        await session.commit()
    return {"status": "OK", "data":new_folder}

@router.put("/{folder_id}")
async def edit_folder(folder_id:int, folder:Folder):
    async with async_session_maker() as session:
        await FoldersRepository(session).edit(folder,id=folder_id)
        await session.commit()
    return {"status":"OK"}

@router.patch("/{folder_id}")
async def part_edit_folder(folder_id:int, folder:FolderPatch):
    async with async_session_maker() as session:
        await FoldersRepository(session).edit(folder,exclude_unset=True,id=folder_id)
        # поля, которые не передали, не учитываются
        await session.commit()
    return {"status":"OK"}

@router.delete("/{folder_id}")
async def delete_folder(folder_id:int):
    async with async_session_maker() as session:
        await FoldersRepository(session).delete(id=folder_id)
        await session.commit()
    return {"status":"OK"}