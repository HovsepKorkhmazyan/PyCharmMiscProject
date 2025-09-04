from fastapi import FastAPI, Header, HTTPException, Request
import re
from typing import Optional

app = FastAPI(title="Headers Demo API", version="1.0.0")


def validate_accept_language(accept_language: str) -> bool:
    pattern = r'^[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9](\.[0-9])?)?(\s*,\s*[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9](\.[0-9])?)?)*$'
    return bool(re.match(pattern, accept_language.replace(' ', '')))


@app.get("/headers")
async def get_headers(
        user_agent: Optional[str] = Header(None, alias="User-Agent"),
        accept_language: Optional[str] = Header(None, alias="Accept-Language")
):
    if not user_agent:
        raise HTTPException(
            status_code=400,
            detail="User-Agent header is required"
        )

    if not accept_language:
        raise HTTPException(
            status_code=400,
            detail="Accept-Language header is required"
        )

    if not validate_accept_language(accept_language):
        raise HTTPException(
            status_code=400,
            detail="Accept-Language header has invalid format. Expected format: 'en-US,en;q=0.9,es;q=0.8'"
        )

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }


@app.get("/headers-alt")
async def get_headers_alternative(request: Request):
    headers = request.headers

    user_agent = headers.get("user-agent")
    accept_language = headers.get("accept-language")

    if not user_agent:
        raise HTTPException(
            status_code=400,
            detail="User-Agent header is required"
        )

    if not accept_language:
        raise HTTPException(
            status_code=400,
            detail="Accept-Language header is required"
        )

    if not validate_accept_language(accept_language):
        raise HTTPException(
            status_code=400,
            detail="Accept-Language header has invalid format"
        )

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }


@app.get("/")
async def root():
    return {"message": "Headers Demo API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
