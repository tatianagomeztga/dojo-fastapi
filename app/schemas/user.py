from typing import Optional

from pydantic import BaseModel


class SearchUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None


class UserIn(BaseModel):
    name: str
    age: int
    is_active: bool


class UserOut(BaseModel):
    name: str
    age: int