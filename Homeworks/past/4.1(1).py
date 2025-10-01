from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import PlainTextResponse
import secrets

app = FastAPI()
security = HTTPBasic()

VALID_USERNAME = "user1"
VALID_PASSWORD = "password123"


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/Login", response_class=PlainTextResponse)
def login(username: str = Depends(verify_credentials)):
    return "You Got My Secret, Welcome"
