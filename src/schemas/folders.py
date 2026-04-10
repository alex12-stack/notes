from pydantic import BaseModel, Field

class Folder(BaseModel):
    name: str
    owner_id: int

class FolderPatch(BaseModel):
    name: str | None = Field(None)
    owner_id: int | None = Field(None)
