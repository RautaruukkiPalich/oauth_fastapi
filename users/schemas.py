from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserAuth(User):
    password: str


class UserData(User):
    id: int | None
    created_at: datetime | None
    last_password_change: datetime | None


class ChangePassword(BaseModel):
    old_password: str
    new_password1: str
    new_password2: str
