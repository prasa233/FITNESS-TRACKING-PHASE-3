
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.phase3 import WaterTracking
from app.schemas.phase3 import WaterCreate, WaterResponse, WaterProgress


router = APIRouter(
    prefix="/phase3/water",
    tags=["Water Tracking"]
)

DAILY_WATER_GOAL = 3000


@router.post("/log", response_model=WaterResponse, status_code=201)
def log_water(
    data: WaterCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    record = WaterTracking(
        user_id=user.id,
        quantity=data.quantity,
        date=date.today()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get("/logs", response_model=list[WaterResponse])
def get_water_logs(
    selected_date: date | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(WaterTracking).filter(
        WaterTracking.user_id == user.id
    )

    if selected_date:
        query = query.filter(
            WaterTracking.date == selected_date
        )

    return query.order_by(WaterTracking.date.desc()).all()


@router.get("/daily-progress", response_model=WaterProgress)
def daily_water_progress(
    selected_date: date | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    selected_date = selected_date or date.today()

    total = db.query(
        func.coalesce(func.sum(WaterTracking.quantity), 0)
    ).filter(
        WaterTracking.user_id == user.id,
        WaterTracking.date == selected_date
    ).scalar()

    total = int(total)

    return WaterProgress(
        date=selected_date,
        consumed_ml=total,
        goal_ml=DAILY_WATER_GOAL,
        remaining_ml=max(DAILY_WATER_GOAL - total, 0),
        progress_percentage=round(
            min(total / DAILY_WATER_GOAL * 100, 100), 2
        )
    )


@router.delete("/logs/{record_id}")
def delete_water_log(
    record_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    record = db.query(WaterTracking).filter(
        WaterTracking.id == record_id,
        WaterTracking.user_id == user.id
    ).first()

    if not record:
        raise HTTPException(404, "Water record not found")

    db.delete(record)
    db.commit()

    return {"message": "Water record deleted successfully"}
