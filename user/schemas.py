from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    pass


class UserAuth(User):
    username: str
    password: str


class UserData(User):
    id: int
    username: str
    created_at: datetime
    last_password_change: datetime
