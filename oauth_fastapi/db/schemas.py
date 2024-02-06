from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    username: str
    password: str
