from pydantic import BaseModel

class AuthRequest(BaseModel):
    username: str
    password: str



class SignUpRequest(AuthRequest):
    password_repeat: str



class UserBase(BaseModel):
    id: int
    username: str



class SignUpResponse(BaseModel):
    user: UserBase
    token: str
    


class ListRequest(BaseModel):
    name: str
    description: str | None

class AddBookToListRequest(BaseModel):
    list_id: int
    book_id: int


class ListResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str