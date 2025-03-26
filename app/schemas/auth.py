from pydantic import BaseModel, ConfigDict
from app.schemas.role import RoleResponse

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    role_id: int  # Accept role_id during registration


class UserDB(UserBase):
    id: int
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)
    role: "RoleResponse"
    model_config = {"from_attributes": True}  # Ensure Pydantic v2 compatibility

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class TokenData(BaseModel):
    username: str = None

class Token(BaseModel):
    access_token: str
    token_type: str

