from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP, String, func

import datetime

from src.db import Base

class UserOrm(Base):
    __tablename__ = "Users"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username:Mapped[str] = mapped_column(String(30))
    email:Mapped[str] = mapped_column(String(50),unique=True)
    hashed_password:Mapped[str] = mapped_column(String(500))

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
    )
