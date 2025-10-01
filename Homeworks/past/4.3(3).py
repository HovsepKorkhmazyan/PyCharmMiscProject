from fastapi import FastAPI, Depends, HTTPException, status, Request, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List, Dict, Callable
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

app = FastAPI(title="FastAPI RBAC + Object-Level Access Control")

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
    "user": {"read", "update", "create"},
    "guest": {"read"},
}

# Resource storage: username -> resource dict
resources = {
    "Alice": {"content": "Secret data Alice", "is_public": False},
    "Bob": {"content": "Public notes of Bob", "is_public": True},
    "Admin": {"content": "Administ resource", "is_public": False},
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


def ownership_checker(
        method: str,
        username_path_param: str = "username"
) -> Callable:
    async def checker(
            request: Request,
            current_user: TokenData = Depends(get_current_user),
            username: str = Path(..., alias=username_path_param)
    ):

        if current_user.role == "administrator":
            return

        resource = resources.get(username)
        if resource is None:
            raise HTTPException(status_code=404, detail="Resource not found")

        if current_user.role == "guest":
            if method != "GET":
                raise HTTPException(status_code=403, detail="Guests cannot modify resources")
            if not resource.get("is_public", False):
                raise HTTPException(status_code=403, detail="Guests can only access public resources")
            return

        if current_user.role == "user":
            if method == "GET":
                if resource.get("is_public", False) or username == current_user.username:
                    return
                else:
                    raise HTTPException(status_code=403, detail="Access denied to resource")
            elif method == "POST":

                if username != current_user.username:
                    raise HTTPException(status_code=403, detail="Users can only create their own resource")
                return
            elif method in ("PUT", "DELETE"):
                if username == current_user.username:
                    return
                else:
                    raise HTTPException(status_code=403, detail="Users can only modify their own resource")
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

        raise HTTPException(status_code=403, detail="Access denied")

    return checker


@app.get("/admin")
@require_roles(["administrator"])
@limiter.limit(get_rate_limit_by_role)
async def admin_endpoint(user: TokenData = Depends(get_current_user)):
    return {"message": f"Hello Admin {user.username}"}


@app.get("/user")
@require_roles(["administrator", "user"])
@limiter.limit(get_rate_limit_by_role)
async def user_endpoint(user: TokenData = Depends(get_current_user)):
    return {"message": f"Hello User {user.username}"}


@app.get("/guest")
@require_roles(["administrator", "user", "guest"])
@limiter.limit(get_rate_limit_by_role)
async def guest_endpoint(user: TokenData = Depends(get_current_user)):
    return {"message": f"Hello Guest {user.username}"}


@app.get("/protected_resource/{username}")
@require_roles(["administrator", "user", "guest"])
@limiter.limit(get_rate_limit_by_role)
@ownership_checker("GET")
async def get_resource(username: str, user: TokenData = Depends(get_current_user)):
    resource = resources.get(username)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {
        "owner": username,
        "content": resource["content"],
        "is_public": resource["is_public"]
    }


class ResourceCreateUpdate(BaseModel):
    content: str
    is_public: bool = False


@app.post("/protected_resource/{username}", status_code=201)
@require_roles(["administrator", "user"])
@limiter.limit(get_rate_limit_by_role)
@ownership_checker("POST")
async def create_resource(username: str, data: ResourceCreateUpdate, user: TokenData = Depends(get_current_user)):
    if username in resources:
        raise HTTPException(status_code=409, detail="Resource already exists")
    resources[username] = {"content": data.content, "is_public": data.is_public}
    return {"message": f"Resource created for {username}"}


@app.put("/protected_resource/{username}")
@require_roles(["administrator", "user"])
@limiter.limit(get_rate_limit_by_role)
@ownership_checker("PUT")
async def update_resource(username: str, data: ResourceCreateUpdate, user: TokenData = Depends(get_current_user)):
    resource = resources.get(username)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    resource["content"] = data.content
    resource["is_public"] = data.is_public
    return {"message": f"Resource updated for {username}"}


@app.delete("/protected_resource/{username}")
@require_roles(["administrator", "user"])
@limiter.limit(get_rate_limit_by_role)
@ownership_checker("DELETE")
async def delete_resource(username: str, user: TokenData = Depends(get_current_user)):
    if username not in resources:
        raise HTTPException(status_code=404, detail="Resource not found")
    del resources[username]
    return {"message": f"Resource deleted for {username}"}


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
