import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateNote(BaseModel):
    content: str = Field(min_length=1)
    title: str = Field(min_length=1,max_length=100)
    folder_id: int | None = None
    is_public: bool = False

class Note(CreateNote):
    id: int
    owner_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class GetNotesFiltered(BaseModel):
    content: str | None = None
    title: str | None = None
    is_public: bool | None = None
    folder_id: int | None = None
    created_at: datetime.datetime | None = None


class PatchNote(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)
    folder_id: int | None = None
    is_public: bool | None = None

class CreateNoteDB(CreateNote):
    owner_id: int