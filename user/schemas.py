from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserAuth(User):
    password: str


class UserData(User):
    id: int
    created_at: datetime
    last_password_change: datetime
