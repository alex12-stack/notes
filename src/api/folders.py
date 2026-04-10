from fastapi import Query, APIRouter

from src.schemas.folders import Folder, FolderPatch
from src.repositories.folders import FoldersRepository
from src.api.dependencies import PaginationDep
from src.db import async_session_maker


router = APIRouter(prefix="/folders")

@router.get("")
async def get_folders(
        pagination:PaginationDep,
        name: str | None = Query(None, description="Название папки"),
        owner_id: int | None = Query(None, description="Имя владельца"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await FoldersRepository(session).get_all(
            name=name,
            owner_id=owner_id,
            limit=per_page,
            offset=per_page*(pagination.page-1)
        )

@router.post("")
async def create_folder(folder:Folder):
    async with async_session_maker() as session:
        new_folder = await FoldersRepository(session).add(folder)
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