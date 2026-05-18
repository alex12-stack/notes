import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateFolder(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    owner_id: int

class PatchFolder(BaseModel):
    name: str = Field(min_length=1, max_length=30)


class Folder(CreateFolder):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)