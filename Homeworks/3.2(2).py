from fastapi import FastAPI, HTTPException, Depends, Response, Request
from pydantic import BaseModel
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import uuid
from typing import Dict, Optional

app = FastAPI()

SECRET_KEY = ""
serializer = URLSafeTimedSerializer(SECRET_KEY)

valid_users = {
    "user123": "password123",
    "admin": "admin123",
    "testuser": "testpass"
}

user_data = {
    "user123": {
        "user_id": str(uuid.uuid4()),
        "username": "user123",
        "email": "user123@example.com",
        "full_name": "John Doe",
        "role": "user"
    },
    "admin": {
        "user_id": str(uuid.uuid4()),
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "role": "administrator"
    },
    "testuser": {
        "user_id": str(uuid.uuid4()),
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "role": "user"
    }
}

user_id_to_username = {data["user_id"]: username for username, data in user_data.items()}


class LoginRequest(BaseModel):
    username: str
    password: str


class UserProfile(BaseModel):
    user_id: str
    username: str
    email: str
    full_name: str
    role: str


def get_current_user_id(request: Request) -> str:
    session_token = request.cookies.get("session_token")

    if not session_token:
        raise HTTPException(
            status_code=401,
            detail={"message": "Unauthorized"}
        )

    try:
        user_id = serializer.loads(session_token, max_age=3600)
        return user_id
    except (BadSignature, SignatureExpired):
        raise HTTPException(
            status_code=401,
            detail={"message": "Unauthorized"}
        )


@app.post("/login")
def login(login_data: LoginRequest, response: Response):
    username = login_data.username
    password = login_data.password

    if username not in valid_users or valid_users[username] != password:
        raise HTTPException(
            status_code=401,
            detail={"message": "Invalid credentials"}
        )

    user_id = user_data[username]["user_id"]

    signed_token = serializer.dumps(user_id)

    response.set_cookie(
        key="session_token",
        value=signed_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=3600
    )

    return {
        "message": "Login successful",
        "username": username,
        "user_id": user_id
    }


@app.get("/profile", response_model=UserProfile)
def get_profile(current_user_id: str = Depends(get_current_user_id)):
    if current_user_id not in user_id_to_username:
        raise HTTPException(
            status_code=404,
            detail={"message": "User not found"}
        )

    username = user_id_to_username[current_user_id]
    return user_data[username]


@app.get("/user", response_model=UserProfile)
def get_user_profile(current_user_id: str = Depends(get_current_user_id)):
    if current_user_id not in user_id_to_username:
        raise HTTPException(
            status_code=404,
            detail={"message": "User not found"}
        )

    username = user_id_to_username[current_user_id]
    return user_data[username]


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}


@app.get("/")
def root():
    return {
        "message": "FastAPI Signed Cookie Authentication",
        "endpoints": {
            "login": "POST /login",
            "profile": "GET /profile",
            "user": "GET /user",
            "logout": "POST /logout"
        }
    }


@app.get("/debug/verify-token")
def verify_token_debug(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        return {"error": "No token found"}

    try:
        user_id = serializer.loads(session_token, max_age=3600)
        return {
            "valid": True,
            "user_id": user_id,
            "token_parts": session_token.split('.')
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
