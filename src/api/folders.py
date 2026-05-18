from fastapi import Query, APIRouter, HTTPException

from src.schemas.folders import CreateFolder, PatchFolder, Folder
from src.api.dependencies import PaginationDep
from src.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/folders",tags=["Папки"])

@router.get("", response_model=list[Folder])
async def get_folders(
        pagination:PaginationDep,
        user_id: UserIdDep,
        db: DBDep,
        name: str | None = Query(None, description="Название папки"),
):
    per_page = pagination.per_page or 5
    res = await db.folders.get_all(
        owner_id=user_id,
        name=name,
        limit=per_page,
        offset=per_page*(pagination.page-1),
    )
    return res

@router.post("", response_model=Folder)
async def create_folder(
        user_id: UserIdDep,
        db: DBDep,
        folder: PatchFolder,
):
    new_folder = await db.folders.add(
        CreateFolder(
            owner_id=user_id,
            name=folder.name,
        )
    )
    await db.commit()
    return new_folder


@router.patch("/{folder_id}")
async def patch_folder(
        folder_id: int,
        folder: PatchFolder,
        user_id: UserIdDep,
        db: DBDep,
):
    res = await db.folders.edit(
        data=folder,
        exclude_unset=True,
        id=folder_id,
        owner_id=user_id,
    )
    if res == 0:
        raise HTTPException(status_code=404, detail="Такой папки нет или у вас нет доступа")
    await db.commit()
    return {"status": "updated"}

@router.delete("/{folder_id}")
async def delete_folder(
        folder_id:int,
        user_id: UserIdDep,
        db: DBDep,
):
    res = await db.folders.delete(
        owner_id=user_id,
        id=folder_id,
    )
    if res == 0:
        raise HTTPException(status_code=404,detail="Такой папки нет или у вас нет доступа")
    await db.commit()
    return {"status":"deleted"}