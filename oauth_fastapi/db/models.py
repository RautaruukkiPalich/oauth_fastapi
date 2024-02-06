from datetime import datetime

from sqlalchemy import (
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from oauth_fastapi.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)  # , blank=False)
    password: Mapped[str] = mapped_column(nullable=False)  # , blank=False)
    is_active: Mapped[bool] = mapped_column(default=True)  # , nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_id'),
    )
