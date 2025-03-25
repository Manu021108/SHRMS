from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None



class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserDB(UserBase):
    id: str
    hashed_password: str  # This field exists in MongoDB

class UserResponse(UserBase):
    heashed_password: str   

class User(UserBase):
    id: str

    class Config:
        orm_mode = True