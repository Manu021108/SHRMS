from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.auth import UserCreate, UserResponse, Token, TokenData
from app.core.config import settings
from app.services.authService import create_access_token, decode_access_token, get_user, authenticate_user, create_user
from app.db.database import get_db
from app.models.role import Role
from jose import JWTError

router = APIRouter()

# OAuth2 Scheme (Token-Only Authentication)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Authenticate user using only the JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user

# ✅ Allow multiple roles
def check_role(*required_roles: str):
    def role_checker(current_user: UserResponse = Depends(get_current_active_user)):
        if current_user.role.name not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the required permissions",
            )
        return current_user
    return role_checker

@router.post("/users/", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # ✅ Check if the provided role exists
    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role ID")
    
    return create_user(db, user)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}  # ✅ Fix syntax error
