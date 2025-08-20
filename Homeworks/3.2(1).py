from fastapi import FastAPI, HTTPException, Depends, Response, Request
from pydantic import BaseModel
import uuid
from typing import Dict, Optional

app = FastAPI()

valid_users = {
    "user123": "password123",
    "admin": "admin123",
    "testuser": "testpass"
}

active_sessions: Dict[str, str] = {}

user_profiles = {
    "user123": {
        "username": "user123",
        "email": "user123@example.com",
        "full_name": "John Doe",
        "role": "user"
    },
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "role": "administrator"
    },
    "testuser": {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "role": "user"
    }
}


class LoginRequest(BaseModel):
    username: str
    password: str


class UserProfile(BaseModel):
    username: str
    email: str
    full_name: str
    role: str


def get_current_user(request: Request) -> str:
    session_token = request.cookies.get("SESSION_TOKEN")

    if not session_token:
        raise HTTPException(
            status_code=401,
            detail={"message": "Unauthorized"}
        )

    username = active_sessions.get(session_token)
    if not username:
        raise HTTPException(
            status_code=401,
            detail={"message": "Unauthorized"}
        )

    return username


@app.post("/login")
def login(login_data: LoginRequest, response: Response):
    username = login_data.username
    password = login_data.password

    if username not in valid_users or valid_users[username] != password:
        raise HTTPException(
            status_code=401,
            detail={"message": "Invalid credentials"}
        )

    session_token = str(uuid.uuid4())

    active_sessions[session_token] = username

    response.set_cookie(
        key="SESSION_TOKEN",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=3600
    )

    return {
        "message": "Login successful",
        "username": username
    }


@app.get("/user", response_model=UserProfile)
def get_user_profile(current_user: str = Depends(get_current_user)):
    if current_user not in user_profiles:
        raise HTTPException(
            status_code=404,
            detail={"message": "User profile not found"}
        )

    return user_profiles[current_user]


@app.post("/logout")
def logout(request: Request, response: Response):
    session_token = request.cookies.get("SESSION_TOKEN")

    if session_token and session_token in active_sessions:
        del active_sessions[session_token]

    response.delete_cookie("SESSION_TOKEN")

    return {"message": "Logged out successfully"}


@app.get("/")
def root():
    return {
        "message": "FastAPI Cookie Authentication Demo",
        "endpoints": {
            "login": "POST /login",
            "user_profile": "GET /user",
            "logout": "POST /logout"
        }
    }


@app.get("/debug/sessions")
def get_active_sessions():
    return {
        "active_sessions": len(active_sessions),
        "sessions": active_sessions
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
