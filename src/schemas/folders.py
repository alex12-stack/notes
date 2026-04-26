from pydantic import BaseModel

class CreateFolder(BaseModel):
    name: str

class PatchFolder(BaseModel):
    name: str | None = None
