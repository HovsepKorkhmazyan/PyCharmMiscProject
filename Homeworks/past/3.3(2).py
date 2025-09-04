from fastapi import FastAPI, Header, HTTPException, Response, Depends
from pydantic import BaseModel, Field, validator
from datetime import datetime
import re

app = FastAPI(title="Headers Demo API with Pydantic", version="2.0.0")


class CommonHeaders(BaseModel):
    user_agent: str = Field(..., description="User-Agent header containing browser/client information", min_length=1)
    accept_language: str = Field(..., description="Accept-Language header containing preferred languages", min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "accept_language": "en-US,en;q=0.9,es;q=0.8"
            }
        }

    @validator('accept_language')
    def validate_accept_language_format(cls, v):
        if not v:
            raise ValueError("Accept-Language cannot be empty")

        clean_value = v.replace(' ', '')
        pattern = r'^[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9](\.[0-9])?)?(\s*,\s*[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=[0-9](\.[0-9])?)?)*$'

        if not re.match(pattern, clean_value):
            raise ValueError("Accept-Language header has invalid format. Expected format: 'en-US,en;q=0.9,es;q=0.8'")

        return v


def create_common_headers_dependency():
    async def get_headers(
            user_agent: str = Header(..., alias="User-Agent"),
            accept_language: str = Header(..., alias="Accept-Language")
    ) -> CommonHeaders:
        try:
            return CommonHeaders(user_agent=user_agent, accept_language=accept_language)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return get_headers


common_headers_dep = create_common_headers_dependency()


@app.get("/headers")
async def get_headers_route(
        user_agent: str = Header(..., alias="User-Agent"),
        accept_language: str = Header(..., alias="Accept-Language")
):
    try:
        headers = CommonHeaders(user_agent=user_agent, accept_language=accept_language)
        return {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/info")
async def get_info_route(
        response: Response,
        user_agent: str = Header(..., alias="User-Agent"),
        accept_language: str = Header(..., alias="Accept-Language")
):
    try:
        headers = CommonHeaders(user_agent=user_agent, accept_language=accept_language)
        current_time = datetime.now().isoformat()
        response.headers["X-Server-Time"] = current_time

        return {
            "message": "Welcome! Your headers are successfully processed.",
            "headers": {
                "User-Agent": headers.user_agent,
                "Accept-Language": headers.accept_language
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/headers-clean")
async def get_headers_clean(headers: CommonHeaders = Depends(common_headers_dep)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }


@app.get("/info-clean")
async def get_info_clean(
        response: Response,
        headers: CommonHeaders = Depends(common_headers_dep)
):
    current_time = datetime.now().isoformat()
    response.headers["X-Server-Time"] = current_time

    return {
        "message": "Welcome! Your headers are successfully processed.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }


@app.get("/")
async def root():
    return {
        "message": "Headers Demo API with Pydantic is running",
        "version": "2.0.0",
        "endpoints": ["/headers", "/info", "/headers-clean", "/info-clean"]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
