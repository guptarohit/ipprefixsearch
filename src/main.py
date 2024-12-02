from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="IP Prefix Lookup Service",
    description="Service to lookup IP addresses and find their associated cloud providers and tags",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")
