from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from typing import Dict
import secrets

app = FastAPI()


class UserBase(BaseModel):
    username: str = Field(..., min_length=1)


class User(UserBase):
    password: str = Field(..., min_length=1)


class UserInDB(UserBase):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db: Dict[str, UserInDB] = {}

security = HTTPBasic()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)) -> UserBase:
    username = credentials.username
    password = credentials.password

    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not (secrets.compare_digest(username, user.username) and verify_password(password, user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return UserBase(username=user.username)


@app.post("/register")
def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(username=user.username, hashed_password=hashed_password)
    fake_users_db[user.username] = user_in_db
    return {"message": f"User  '{user.username}' successfully registered."}


@app.get("/login")
def login(current_user: UserBase = Depends(authenticate_user)):
    return {"message": f"Welcome, {current_user.username}!"}
