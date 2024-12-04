"""
API entrypoint for backend API.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

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

# Agent pool keyed by session_id to retain memories/history in-memory.
# Note: the context is lost every time the service is restarted.
agent_pool = {}

@app.get("/")
def root():
    """
    Redirect to the API documentation.
    """
    return RedirectResponse(url="/docs")

@app.get("/status")
def root():
    """
    Health probe endpoint.
    """
    return {"status": "ready"}
