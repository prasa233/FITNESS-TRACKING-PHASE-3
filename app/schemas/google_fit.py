from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter()

class GoogleFitConnectRequest(BaseModel):
    code: str

@router.post("/phase3/integrations/google_fit/connect")
async def connect_google_fit(request: GoogleFitConnectRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Authorization code is required")

    # Exchange the code for tokens using your configured OAuth client.
    # Keep client secrets on the server; do not send them from the browser.
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": request.code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )

    if response.is_error:
        raise HTTPException(
            status_code=400,
            detail=f"Google token exchange failed: {response.text}",
        )

    return response.json()