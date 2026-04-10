from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, ForeignKey

from src.db import Base

import enum


class Role(enum.Enum):
    CREATOR = "creator"
    EDITOR = "editor"
    VIEWER = "viewer"


class NoteAccessOrm(Base):
    __tablename__ = "Note Access"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    note_id:Mapped[int] = mapped_column(ForeignKey("Notes.id"))
    user_id:Mapped[int] = mapped_column(ForeignKey("Users.id"))
    role:Mapped[Role] = mapped_column(Enum(Role))