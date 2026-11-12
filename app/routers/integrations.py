from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.security import get_current_user
from app.core.database import get_db
from app.models import FitnessIntegration, SyncedActivity
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
router = APIRouter(prefix="/phase3/integrations", tags=["Fitness Integrations"])
# ==========================================
# PYDANTIC REQUEST MODELS
# ==========================================

class IntegrationConnect(BaseModel):
    provider: str = Field(
        pattern="^(GOOGLE_FIT|APPLE_HEALTH)$"
    )
    external_user_id: Optional[str] = None

class ActivitySyncRequest(BaseModel):
    activity_type: str = Field(min_length=1, max_length=100)
    steps: int = Field(default=0, ge=0)
    distance: float = Field(default=0, ge=0)
    calories_burned: float = Field(default=0, ge=0)
    activity_date: date
    external_activity_id: Optional[str] = None

# ==========================================
# AUTHENTICATED USER VALIDATION
# ==========================================

def get_user_id(current_user):
    if isinstance(current_user, dict):
        user_id = current_user.get("id") or current_user.get("user_id")
    else:
        user_id = getattr(current_user, "id", None)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authenticated user"
        )

    return int(user_id)

# ==========================================
# MODULE 17: CONNECT INTEGRATION
# ==========================================
class ConnectRequest(BaseModel):
    authorization_code: str = Field(min_length=1)
    redirect_uri: str = Field(min_length=1)

@router.post("/{provider}/connect")
async def connect_integration(
    provider: str,
    body: ConnectRequest,  # This annotation makes `body` a JSON request body.
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user_id = get_user_id(current_user)
    provider = provider.strip().upper()

    if provider != "GOOGLE_FIT":
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported provider: {provider}",
        )

    integration = db.query(FitnessIntegration).filter(
        FitnessIntegration.user_id == user_id,
        FitnessIntegration.provider == provider,
    ).first()

    if integration:
        integration.is_connected = True
    else:
        integration = FitnessIntegration(
            user_id=user_id,
            provider=provider,
            external_user_id=None,
            is_connected=True,
        )
        db.add(integration)

    db.commit()
    db.refresh(integration)

    return {
        "message": "Google Fit connected successfully",
        "integration_id": integration.id,
        "provider": integration.provider,
        "is_connected": integration.is_connected,
    }
# ==========================================
# LIST CONNECTED INTEGRATIONS
# ==========================================

@router.get("/")
def list_integrations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = get_user_id(current_user)

    integrations = db.query(FitnessIntegration).filter(
        FitnessIntegration.user_id == user_id
    ).all()

    return [
        {
            "id": item.id,
            "provider": item.provider,
            "is_connected": item.is_connected,
            "last_synced_at": item.last_synced_at
        }
        for item in integrations
    ]

# ==========================================
# DISCONNECT INTEGRATION
# ==========================================

@router.delete("/{integration_id}/disconnect")
def disconnect_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user_id = get_user_id(current_user)

    integration = db.query(FitnessIntegration).filter(
        FitnessIntegration.id == integration_id,
        FitnessIntegration.user_id == user_id,
    ).first()

    if integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")

    integration.is_connected = False
    integration.access_token_encrypted = None
    integration.refresh_token_encrypted = None

    db.commit()

    return {"message": "Integration disconnected successfully"}
# ==========================================
# MODULE 17: SYNC ACTIVITY DATA
# ==========================================

@router.post("/{provider}/sync")
def sync_activity(
    provider: str,
    data: ActivitySyncRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = get_user_id(current_user)
    provider = provider.upper()

    integration = db.query(FitnessIntegration).filter(
        FitnessIntegration.user_id == user_id,
        FitnessIntegration.provider == provider,
        FitnessIntegration.is_connected == True
    ).first()

    if not integration:
        raise HTTPException(
            status_code=404,
            detail="Please connect your fitness integration first"
        )

    if data.external_activity_id:
        existing = db.query(SyncedActivity).filter(
            SyncedActivity.integration_id == integration.id,
            SyncedActivity.external_activity_id == data.external_activity_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Activity already synchronized"
            )

    activity = SyncedActivity(
        user_id=user_id,
        integration_id=integration.id,
        activity_type=data.activity_type,
        steps=data.steps,
        distance=data.distance,
        calories_burned=data.calories_burned,
        activity_date=data.activity_date,
        external_activity_id=data.external_activity_id
    )

    integration.last_synced_at = datetime.utcnow()

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return {
        "message": "Activity synchronized successfully",
        "activity_id": activity.id,
        "provider": provider,
        "steps": activity.steps,
        "distance": activity.distance,
        "calories_burned": activity.calories_burned
    }

# ==========================================
# VIEW SYNCHRONIZED ACTIVITIES
# ==========================================

@router.get("/activities")
def get_synced_activities(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = get_user_id(current_user)

    activities = db.query(SyncedActivity).filter(
        SyncedActivity.user_id == user_id
    ).order_by(
        SyncedActivity.activity_date.desc()
    ).all()

    return [
        {
            "id": item.id,
            "activity_type": item.activity_type,
            "steps": item.steps,
            "distance": item.distance,
            "calories_burned": item.calories_burned,
            "activity_date": item.activity_date,
            "integration_id": item.integration_id
        }
        for item in activities
    ]