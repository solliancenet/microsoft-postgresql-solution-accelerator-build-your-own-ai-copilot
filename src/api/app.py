"""
API entrypoint for backend API.
"""
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from config import KeyVaultConfigProvider

import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

# Initialize Key Vault Config Provider
config_provider = KeyVaultConfigProvider()


app = FastAPI(docs_url="/")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from api.v1.status import router as api_v1_status_router
from api.v1.documents import router as api_v1_documents_router
from api.v1.company import router as api_v1_company_router

app.include_router(api_v1_status_router, prefix="/v1", tags=["Status"])
app.include_router(api_v1_documents_router, prefix="/v1", tags=["Documents"])
app.include_router(api_v1_company_router, prefix="/v1", tags=["Company"])


# Agent pool keyed by session_id to retain memories/history in-memory.
# Note: the context is lost every time the service is restarted.
agent_pool = {}
