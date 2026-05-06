import datetime

from pydantic import BaseModel, ConfigDict


class CreateFolder(BaseModel):
    name: str
    owner_id: int

class PatchFolder(BaseModel):
    name: str


class Folder(CreateFolder):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)