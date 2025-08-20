from fastapi import FastAPI, HTTPException, Depends, Response, Request
from pydantic import BaseModel
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import uuid
import time
from typing import Dict, Optional

app = FastAPI()

SECRET_KEY = ""
serializer = URLSafeTimedSerializer(SECRET_KEY)

SESSION_TIMEOUT = 300
EXTENSION_THRESHOLD = 180

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


class SessionData(BaseModel):
    user_id: str
    last_activity: float
    should_update: bool = False


def create_session_token(user_id: str, timestamp: float) -> str:
    session_data = f"{user_id}.{timestamp}"
    return serializer.dumps(session_data)


def parse_session_token(token: str) -> SessionData:
    try:
        session_data = serializer.loads(token)
        parts = session_data.split('.')

        if len(parts) != 2:
            raise ValueError("Invalid token format")

        user_id = parts[0]
        last_activity = float(parts[1])

        if user_id not in user_id_to_username:
            raise ValueError("Invalid user ID")

        current_time = time.time()
        time_since_activity = current_time - last_activity

        if time_since_activity > SESSION_TIMEOUT:
            raise ValueError("Session expired")

        should_update = time_since_activity >= EXTENSION_THRESHOLD

        return SessionData(
            user_id=user_id,
            last_activity=last_activity,
            should_update=should_update
        )

    except (BadSignature, SignatureExpired, ValueError, TypeError):
        raise ValueError("Invalid session")


def get_current_session(request: Request, response: Response) -> SessionData:
    session_token = request.cookies.get("session_token")

    if not session_token:
        response.status_code = 401
        raise HTTPException(
            status_code=401,
            detail={"message": "Session expired"}
        )

    try:
        session_data = parse_session_token(session_token)

        if session_data.should_update:
            current_time = time.time()
            new_token = create_session_token(session_data.user_id, current_time)

            response.set_cookie(
                key="session_token",
                value=new_token,
                httponly=True,
                secure=False,
                samesite="strict",
                max_age=SESSION_TIMEOUT
            )

            session_data.last_activity = current_time

        return session_data

    except ValueError as e:
        if "expired" in str(e):
            response.status_code = 401
            raise HTTPException(
                status_code=401,
                detail={"message": "Session expired"}
            )
        else:
            response.status_code = 401
            raise HTTPException(
                status_code=401,
                detail={"message": "Invalid session"}
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
    current_time = time.time()

    session_token = create_session_token(user_id, current_time)

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=SESSION_TIMEOUT
    )

    return {
        "message": "Login successful",
        "username": username,
        "user_id": user_id,
        "session_expires_in": SESSION_TIMEOUT
    }


@app.get("/profile", response_model=UserProfile)
def get_profile(session_data: SessionData = Depends(get_current_session)):
    username = user_id_to_username[session_data.user_id]
    return user_data[username]


@app.get("/user", response_model=UserProfile)
def get_user_profile(session_data: SessionData = Depends(get_current_session)):
    username = user_id_to_username[session_data.user_id]
    return user_data[username]


@app.get("/protected")
def protected_route(session_data: SessionData = Depends(get_current_session)):
    username = user_id_to_username[session_data.user_id]
    current_time = time.time()
    time_since_activity = current_time - session_data.last_activity

    return {
        "message": f"Hello {username}",
        "user_id": session_data.user_id,
        "time_since_last_activity": round(time_since_activity, 2),
        "session_updated": session_data.should_update,
        "current_timestamp": current_time
    }


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}


@app.get("/")
def root():
    return {
        "message": "FastAPI Dynamic Session Authentication",
        "session_config": {
            "timeout_seconds": SESSION_TIMEOUT,
            "extension_threshold_seconds": EXTENSION_THRESHOLD,
            "session_format": "user_id.timestamp.signature"
        },
        "endpoints": {
            "login": "POST /login",
            "profile": "GET /profile",
            "user": "GET /user",
            "protected": "GET /protected",
            "logout": "POST /logout"
        }
    }


@app.get("/debug/session-info")
def session_info(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        return {"error": "No session token found"}

    try:
        session_data = parse_session_token(session_token)
        current_time = time.time()
        time_since_activity = current_time - session_data.last_activity

        return {
            "valid": True,
            "user_id": session_data.user_id,
            "last_activity": session_data.last_activity,
            "current_time": current_time,
            "time_since_activity": round(time_since_activity, 2),
            "should_update": session_data.should_update,
            "expires_in": round(SESSION_TIMEOUT - time_since_activity, 2),
            "token_preview": f"{session_token[:20]}..."
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e),
            "token_preview": f"{session_token[:20]}..." if session_token else None
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
