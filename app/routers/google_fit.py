# app/routers/google_fit.py

from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

router = APIRouter(prefix="/phase3/integrations")

class ConnectRequest(BaseModel):
    redirect_uri: HttpUrl

@router.post("/GOOGLE_FIT/connect")
async def connect_google_fit(request: ConnectRequest):
    # Replace this with the OAuth URL creation used by your app.
    return {
        "provider": "GOOGLE_FIT",
        "redirect_uri": str(request.redirect_uri),
        "status": "connection_started",
    }