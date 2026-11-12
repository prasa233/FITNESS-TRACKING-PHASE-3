
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.phase3 import Reminder, ReminderLog

from app.schemas.phase3 import (
    ReminderCreate,
    ReminderUpdate,
    ReminderResponse,
    ReminderLogResponse
)


router = APIRouter(
    prefix="/phase3/reminders",
    tags=["Reminders"]
)


def calculate_next_run(reminder_time, timezone, repeat_days):
    try:
        tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        raise HTTPException(400, "Invalid timezone")

    now = datetime.now(tz)

    days = repeat_days or list(range(7))

    for offset in range(8):
        candidate_date = (now + timedelta(days=offset)).date()

        if candidate_date.weekday() not in days:
            continue

        candidate = datetime.combine(
            candidate_date,
            reminder_time,
            tzinfo=tz
        )

        if candidate > now:
            return candidate.replace(tzinfo=None)

    return None


@router.post("/", response_model=ReminderResponse, status_code=201)
def create_reminder(
    data: ReminderCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    next_run = calculate_next_run(
        data.reminder_time,
        data.timezone,
        data.repeat_days
    )

    reminder = Reminder(
        user_id=user.id,
        reminder_type=data.reminder_type,
        title=data.title,
        message=data.message,
        reminder_time=data.reminder_time.strftime("%H:%M"),
        timezone=data.timezone,
        repeat_days=data.repeat_days,
        is_active=data.is_active,
        next_run_at=next_run
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder


@router.get("/", response_model=list[ReminderResponse])
def get_reminders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Reminder).filter(
        Reminder.user_id == user.id
    ).order_by(Reminder.created_at.desc()).all()


@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    data: ReminderUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == user.id
    ).first()

    if not reminder:
        raise HTTPException(404, "Reminder not found")

    updates = data.model_dump(exclude_unset=True)

    new_time = updates.get("reminder_time")
    new_timezone = updates.get("timezone", reminder.timezone)
    new_days = updates.get("repeat_days", reminder.repeat_days or [])

    if new_time is not None:
        updates["reminder_time"] = new_time.strftime("%H:%M")

    for key, value in updates.items():
        setattr(reminder, key, value)

    if reminder.is_active:
        from datetime import time as time_type

        parsed_time = (
            new_time
            if new_time is not None
            else time_type.fromisoformat(reminder.reminder_time)
        )

        reminder.next_run_at = calculate_next_run(
            parsed_time,
            new_timezone,
            new_days
        )
    else:
        reminder.next_run_at = None

    db.commit()
    db.refresh(reminder)

    return reminder


@router.patch("/{reminder_id}/toggle")
def toggle_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == user.id
    ).first()

    if not reminder:
        raise HTTPException(404, "Reminder not found")

    reminder.is_active = not reminder.is_active

    if reminder.is_active:
        from datetime import time as time_type

        reminder.next_run_at = calculate_next_run(
            time_type.fromisoformat(reminder.reminder_time),
            reminder.timezone or "Asia/Kolkata",
            reminder.repeat_days or []
        )
    else:
        reminder.next_run_at = None

    db.commit()

    return {
        "message": "Reminder status updated",
        "is_active": reminder.is_active
    }


@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == user.id
    ).first()

    if not reminder:
        raise HTTPException(404, "Reminder not found")

    db.query(ReminderLog).filter(
        ReminderLog.reminder_id == reminder_id,
        ReminderLog.user_id == user.id
    ).delete(synchronize_session=False)

    db.delete(reminder)
    db.commit()

    return {"message": "Reminder deleted successfully"}


@router.get(
    "/history",
    response_model=list[ReminderLogResponse]
)
def reminder_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(ReminderLog).filter(
        ReminderLog.user_id == user.id
    ).order_by(
        ReminderLog.created_at.desc()
    ).all()
