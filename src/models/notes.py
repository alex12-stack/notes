from typing import Literal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, TIMESTAMP ,ForeignKey, func

import datetime

from src.db import Base



class NotesOrm(Base):
    __tablename__ = "Notes"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column(String(100))
    content:Mapped[str] = mapped_column(Text)
    is_public:Mapped[bool] = mapped_column(default=False)
    owner_id:Mapped[int] = mapped_column(ForeignKey("Users.id"))
    folder_id:Mapped[int | None] = mapped_column(
        ForeignKey("Folders.id"),
        nullable=True,
    )

    created_at:Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at:Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )
