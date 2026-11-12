
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.phase3 import WorkoutSession

from app.schemas.phase3 import (
    WorkoutStart,
    WorkoutStop,
    WorkoutSessionResponse,
    WorkoutTimerStatus
)


router = APIRouter(
    prefix="/phase3/timer",
    tags=["Workout Timer"]
)


@router.post("/start", response_model=WorkoutSessionResponse)
def start_workout(
    data: WorkoutStart,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    active = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user.id,
        WorkoutSession.status == "IN_PROGRESS"
    ).first()

    if active:
        raise HTTPException(
            400,
            "You already have an active workout"
        )

    session = WorkoutSession(
        user_id=user.id,
        workout_name=data.workout_name,
        start_time=datetime.utcnow(),
        calories_per_minute=data.calories_per_minute,
        duration_seconds=0,
        calories_burned=0,
        status="IN_PROGRESS"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


@router.get("/active", response_model=WorkoutTimerStatus)
def active_workout(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user.id,
        WorkoutSession.status == "IN_PROGRESS"
    ).first()

    if not session:
        raise HTTPException(404, "No active workout found")

    elapsed = max(
        0,
        int((datetime.utcnow() - session.start_time).total_seconds())
    )

    return WorkoutTimerStatus(
        session_id=session.id,
        workout_name=session.workout_name,
        status=session.status,
        start_time=session.start_time,
        elapsed_seconds=elapsed,
        calories_burned=round(
            elapsed / 60 * session.calories_per_minute, 2
        )
    )


@router.post("/{session_id}/stop", response_model=WorkoutSessionResponse)
def stop_workout(
    session_id: int,
    data: WorkoutStop,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == session_id,
        WorkoutSession.user_id == user.id
    ).first()

    if not session:
        raise HTTPException(404, "Workout session not found")

    if session.status != "IN_PROGRESS":
        raise HTTPException(400, "Workout is already stopped")

    end_time = datetime.utcnow()

    duration = max(
        0,
        int((end_time - session.start_time).total_seconds())
    )

    session.end_time = end_time
    session.duration_seconds = duration
    session.calories_burned = round(
        duration / 60 * session.calories_per_minute, 2
    )
    session.status = data.status

    db.commit()
    db.refresh(session)

    return session


@router.get("/history", response_model=list[WorkoutSessionResponse])
def workout_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user.id
    ).order_by(
        WorkoutSession.start_time.desc()
    ).all()
