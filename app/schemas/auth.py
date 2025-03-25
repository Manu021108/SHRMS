from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserDB(UserBase):
    id: int
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
class TokenData(BaseModel):
    username: str = None

class Token(BaseModel):
    access_token: str
    token_type: str

