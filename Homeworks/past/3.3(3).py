from fastapi import FastAPI, Header, HTTPException, Response, Depends
from pydantic import BaseModel, Field, validator
from datetime import datetime
import re

app = FastAPI(title="Headers Demo API with Version Control", version="2.1.0")

MINIMUM_APP_VERSION = "0.0.2"


def compare_versions(version1: str, version2: str) -> int:
    v1_parts = [int(x) for x in version1.split('.')]
    v2_parts = [int(x) for x in version2.split('.')]

    for i in range(max(len(v1_parts), len(v2_parts))):
        v1_part = v1_parts[i] if i < len(v1_parts) else 0
        v2_part = v2_parts[i] if i < len(v2_parts) else 0

        if v1_part < v2_part:
            return -1
        elif v1_part > v2_part:
            return 1

    return 0


class CommonHeaders(BaseModel):
    user_agent: str = Field(..., description="User-Agent header containing browser/client information", min_length=1)
    accept_language: str = Field(..., description="Accept-Language header containing preferred languages", min_length=1)
    x_current_version: str = Field(
        ...,
        description="X-Current-Version header containing app version",
        regex=r'^\d+\.\d+\.\d+$',
        example="1.0.0"
    )

    class Config:
        schema_extra = {
            "example": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "accept_language": "en-US,en;q=0.9,es;q=0.8",
                "x_current_version": "1.0.0"
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

    @validator('x_current_version')
    def validate_version(cls, v):
        if not v:
            raise ValueError("X-Current-Version cannot be empty")

        version_pattern = r'^\d+\.\d+\.\d+$'
        if not re.match(version_pattern, v):
            raise ValueError("X-Current-Version must follow format: x.y.z (e.g., 1.0.0)")

        if compare_versions(v, MINIMUM_APP_VERSION) < 0:
            raise ValueError("Update the application")

        return v


def create_common_headers_dependency():
    async def get_headers(
            user_agent: str = Header(..., alias="User-Agent"),
            accept_language: str = Header(..., alias="Accept-Language"),
            x_current_version: str = Header(..., alias="X-Current-Version")
    ) -> CommonHeaders:
        try:
            return CommonHeaders(
                user_agent=user_agent,
                accept_language=accept_language,
                x_current_version=x_current_version
            )
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    return get_headers


common_headers_dep = create_common_headers_dependency()


@app.get("/headers")
async def get_headers_route(
        user_agent: str = Header(..., alias="User-Agent"),
        accept_language: str = Header(..., alias="Accept-Language"),
        x_current_version: str = Header(..., alias="X-Current-Version")
):
    try:
        headers = CommonHeaders(
            user_agent=user_agent,
            accept_language=accept_language,
            x_current_version=x_current_version
        )
        return {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/info")
async def get_info_route(
        response: Response,
        user_agent: str = Header(..., alias="User-Agent"),
        accept_language: str = Header(..., alias="Accept-Language"),
        x_current_version: str = Header(..., alias="X-Current-Version")
):
    try:
        headers = CommonHeaders(
            user_agent=user_agent,
            accept_language=accept_language,
            x_current_version=x_current_version
        )
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
        raise HTTPException(status_code=422, detail=str(e))


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


@app.get("/version-info")
async def get_version_info():
    return {
        "minimum_required_version": MINIMUM_APP_VERSION,
        "current_api_version": "2.1.0",
        "message": f"Client app version must be >= {MINIMUM_APP_VERSION}"
    }


@app.get("/")
async def root():
    return {
        "message": "Headers Demo API with Version Control is running",
        "version": "2.1.0",
        "minimum_app_version": MINIMUM_APP_VERSION,
        "endpoints": ["/headers", "/info", "/headers-clean", "/info-clean", "/version-info"]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
