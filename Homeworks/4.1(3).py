import os
import secrets
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse, JSONResponse, PlainTextResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

MODE = os.getenv("MODE", "DEV").upper()
DOCS_USER = os.getenv("DOCS_USER", "devuser")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "devpass")

security = HTTPBasic()


def verify_docs_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, DOCS_USER)
    correct_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect authentication for docs",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


if MODE not in ("DEV", "PROD"):
    raise RuntimeError(f"Invalid MODE environment variable: {MODE}. Must be 'DEV' or 'PROD'.")

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

if MODE == "DEV":
    @app.get("/docs", include_in_schema=False)
    async def get_documentation(username: str = Depends(verify_docs_credentials)):
        return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")


    @app.get("/openapi.json", include_in_schema=False)
    async def openapi(username: str = Depends(verify_docs_credentials)):
        return JSONResponse(get_openapi(title=app.title, version=app.version, routes=app.routes))



    @app.get("/redoc", include_in_schema=False)
    async def redoc():
        return PlainTextResponse("Not Found", status_code=404)

if MODE == "PROD":
    @app.get("/docs", include_in_schema=False)
    async def docs_not_found():
        return PlainTextResponse("Not Found", status_code=404)


    @app.get("/openapi.json", include_in_schema=False)
    async def openapi_not_found():
        return PlainTextResponse("Not Found", status_code=404)


    @app.get("/redoc", include_in_schema=False)
    async def redoc_not_found():
        return PlainTextResponse("Not Found", status_code=404)


@app.get("/")
async def root():
    return {"message": f"Hello! Running in {MODE} mode."}
