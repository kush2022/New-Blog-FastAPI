from pydantic import BaseModel
from typing import List

class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    class Config():
        orm_mode = True



class Blog(BaseModel):
    title: str
    body: str | None = None



# -- users
class User(BaseModel): 
    name: str
    email: str
    password: str



class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None



