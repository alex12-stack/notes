from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP, String

import datetime

from src.db import Base

class UserOrm(Base):
    __tablename__ = "Users"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username:Mapped[str] = mapped_column(String(30))
    email:Mapped[str] = mapped_column(String(50))
    password:Mapped[str] = mapped_column(String(50))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.datetime.now())