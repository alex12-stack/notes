from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, TIMESTAMP ,ForeignKey, Enum

import datetime

from src.db import Base

import enum

class Is_Public(enum.Enum):
    Public="public"
    Private="private"


class NotesOrm(Base):
    __tablename__ = "Notes"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column(String(100))
    content:Mapped[str] = mapped_column(Text)
    is_public:Mapped[Is_Public] = mapped_column(Enum(Is_Public))
    owner_id:Mapped[int] = mapped_column(ForeignKey("Users.id"))
    folder_id:Mapped[int] = mapped_column(ForeignKey("Folders.id"))
    created_at:Mapped[TIMESTAMP] = mapped_column(TIMESTAMP,default=datetime.datetime.now())
    updated_at:Mapped[TIMESTAMP] = mapped_column(TIMESTAMP,default=datetime.datetime.now())
