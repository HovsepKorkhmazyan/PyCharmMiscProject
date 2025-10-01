from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

app = FastAPI(title="FastAPI RBAC with Rate Limiting")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

SECRET_KEY = ""
ALGORITHM = "HS256"
security = HTTPBearer()

fake_users_db = {
    "admin_user": {"username": "admin_user", "role": "administrator"},
    "normal_user": {"username": "normal_user", "role": "user"},
    "guest_user": {"username": "guest_user", "role": "guest"},
}

role_permissions = {
    "administrator": {"create", "read", "update", "delete"},
    "user": {"read", "update"},
    "guest": {"read"},
}


class TokenData(BaseModel):
    username: str
    role: str


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return TokenData(username=username, role=role)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    token = credentials.credentials
    return decode_token(token)


def require_roles(allowed_roles: List[str]):
    def role_checker(current_user: TokenData = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return current_user

    return role_checker


def get_rate_limit_by_role(current_user: TokenData = Depends(get_current_user)) -> str:
    if current_user.role == "administrator":
        return "1000/minute"
    elif current_user.role == "user":
        return "20/minute"
    elif current_user.role == "guest":
        return "5/minute"
    else:
        return "1/minute"


@app.get("/protected_resource")
@require_roles(["administrator", "user"])
@limiter.limit(get_rate_limit_by_role)
async def protected_resource(user: TokenData = Depends(get_current_user)):
    return {"message": f"Hello {user.username}, you have access to this protected resource."}


@app.post("/resource/create")
@require_roles(["administrator"])
@limiter.limit(get_rate_limit_by_role)
async def create_resource(user: TokenData = Depends(get_current_user)):
    return {"message": f"Resource created by {user.username} (role: {user.role})"}


@app.get("/resource/read")
@require_roles(["administrator", "user", "guest"])
@limiter.limit(get_rate_limit_by_role)
async def read_resource(user: TokenData = Depends(get_current_user)):
    return {"message": f"Resource read by {user.username} (role: {user.role})"}


@app.put("/resource/update")
@require_roles(["administrator", "user"])
@limiter.limit(get_rate_limit_by_role)
async def update_resource(user: TokenData = Depends(get_current_user)):
    return {"message": f"Resource updated by {user.username} (role: {user.role})"}


@app.delete("/resource/delete")
@require_roles(["administrator"])
@limiter.limit(get_rate_limit_by_role)
async def delete_resource(user: TokenData = Depends(get_current_user)):
    return {"message": f"Resource deleted by {user.username} (role: {user.role})"}


@app.post("/token/{username}")
async def generate_token(username: str):
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User  not found")
    to_encode = {
        "sub": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
