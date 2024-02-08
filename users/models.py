from datetime import datetime

from sqlalchemy import (
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)  # , blank=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)  # , blank=False)
    last_password_change: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_id'),
    )
