from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey,TIMESTAMP, func

import datetime

from src.db import Base

class FoldersOrm(Base):
    __tablename__ = "Folders"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(30))
    owner_id:Mapped[int] = mapped_column(ForeignKey("Users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=func.now())
