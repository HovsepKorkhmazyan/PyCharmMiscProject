from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

app = FastAPI(title="FastAPI RBAC Example")

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


@app.get("/protected_resource")
def protected_resource(user: TokenData = Depends(require_roles(["administrator", "user"]))):
    return {"message": f"Hello {user.username}, you have access to this protected resource."}


@app.post("/resource/create")
def create_resource(user: TokenData = Depends(require_roles(["administrator"]))):
    return {"message": f"Resource created by {user.username} (role: {user.role})"}


@app.get("/resource/read")
def read_resource(user: TokenData = Depends(require_roles(["administrator", "user", "guest"]))):
    return {"message": f"Resource read by {user.username} (role: {user.role})"}


@app.put("/resource/update")
def update_resource(user: TokenData = Depends(require_roles(["administrator", "user"]))):
    return {"message": f"Resource updated by {user.username} (role: {user.role})"}


@app.delete("/resource/delete")
def delete_resource(user: TokenData = Depends(require_roles(["administrator"]))):
    return {"message": f"Resource deleted by {user.username} (role: {user.role})"}


@app.post("/token/{username}")
def generate_token(username: str):
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    to_encode = {
        "sub": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
