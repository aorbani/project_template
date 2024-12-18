import logging
import os
from typing import Annotated
from .assistant import assistant
import seqlog
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi

from APIs.auth import has_access, get_user

seqlog.log_to_seq(
            server_url=os.getenv('seq_server').replace("code", "dev"),
            api_key=os.getenv("seq_api_key"),
            level=logging.INFO,
            batch_size=1,
            auto_flush_timeout=1,
            override_root_logger=True,
            support_extra_properties=True
        )

logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

app = FastAPI(docs_url="/swagger",redoc_url=None)
@app.on_event("startup")
async def startup_event():
    logging.info("API Application started")
# routes
PROTECTED = [Depends(has_access)]

app.include_router(
    assistant().router,
    dependencies=PROTECTED,
    prefix='/api/v1'
)
@app.get("/", include_in_schema=False)
def root():
    return {"Welcome to AI World! Please to route to /swagger"}
@app.get("/users/me", tags=['User'])
async def read_users_me(current_user: Annotated[dict, Depends(get_user)]):
    return current_user

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Aurora AI APIs",
        version="1.0.0",
        summary="Aurora AI Endpoints",
        description="Here's Aurora AI Endpoints",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "media/ai_logo.jpg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
