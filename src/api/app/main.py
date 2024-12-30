from fastapi import FastAPI
from app.lifespan_manager import lifespan
from app.routers import (
    completions,
    documents,
    embeddings,
    status,
    vendors
)

app = FastAPI(
    lifespan=lifespan,
    title="Build Your Own Copilot with Azure Database for PostgreSQL Solution Accelerator API",
    summary="API for the Build Your Own Copilot with Azure Database for PostgreSQL Solution Accelerator",
    version="1.0.0",
    docs_url="/swagger",
    openapi_url="/swagger/v1/swagger.json"
)

app.include_router(completions.router)
app.include_router(documents.router)
app.include_router(embeddings.router)
app.include_router(status.router)
app.include_router(vendors.router)

@app.get("/")
async def get():
    """API welcome message."""
    return {"message": "Welcome to the Build Your Own Copilot with Azure Database for PostgreSQL Solution Accelerator API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")