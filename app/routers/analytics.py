
from datetime import date, timedelta
import calendar

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.phase3 import WorkoutSession

from app.schemas.phase3 import (
    WeeklyAnalyticsResponse,
    MonthlyAnalyticsResponse,
    DailyWorkoutAnalytics,
    GoalAnalyticsResponse,
    PerformanceInsights
)


router = APIRouter(
    prefix="/phase3/analytics",
    tags=["Advanced Analytics"]
)


def calculate_workout_stats(db, user_id, start_date, end_date):
    sessions = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user_id,
        WorkoutSession.status == "COMPLETED",
        WorkoutSession.start_time >= start_date,
        WorkoutSession.start_time < end_date
    ).all()

    total_workouts = len(sessions)

    total_seconds = sum(
        session.duration_seconds or 0
        for session in sessions
    )

    total_calories = sum(
        session.calories_burned or 0
        for session in sessions
    )

    active_days = len({
        session.start_time.date()
        for session in sessions
    })

    return {
        "sessions": sessions,
        "total_workouts": total_workouts,
        "total_duration_minutes": total_seconds // 60,
        "total_calories_burned": round(total_calories, 2),
        "active_days": active_days
    }


@router.get("/weekly", response_model=WeeklyAnalyticsResponse)
def weekly_analytics(
    selected_date: date | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    selected_date = selected_date or date.today()

    start_date = selected_date - timedelta(
        days=selected_date.weekday()
    )

    end_date = start_date + timedelta(days=7)

    stats = calculate_workout_stats(
        db,
        user.id,
        start_date,
        end_date
    )

    daily = []

    for day_offset in range(7):
        current_day = start_date + timedelta(days=day_offset)

        day_sessions = [
            s for s in stats["sessions"]
            if s.start_time.date() == current_day
        ]

        daily.append(
            DailyWorkoutAnalytics(
                date=current_day,
                workout_count=len(day_sessions),
                duration_minutes=sum(
                    s.duration_seconds or 0
                    for s in day_sessions
                ) // 60,
                calories_burned=round(
                    sum(s.calories_burned or 0 for s in day_sessions),
                    2
                )
            )
        )

    consistency = round(
        stats["active_days"] / 7 * 100, 2
    )

    return WeeklyAnalyticsResponse(
        start_date=start_date,
        end_date=end_date - timedelta(days=1),
        total_workouts=stats["total_workouts"],
        total_duration_minutes=stats["total_duration_minutes"],
        total_calories_burned=stats["total_calories_burned"],
        active_days=stats["active_days"],
        workout_consistency_percentage=consistency,
        daily_breakdown=daily
    )


@router.get("/monthly", response_model=MonthlyAnalyticsResponse)
def monthly_analytics(
    year: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    today = date.today()

    year = year or today.year
    month = month or today.month

    if year < 2000 or year > 2100 or month < 1 or month > 12:
        raise HTTPException(400, "Invalid year or month")

    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    stats = calculate_workout_stats(
        db,
        user.id,
        start_date,
        end_date
    )

    days_in_month = calendar.monthrange(year, month)[1]

    consistency = round(
        stats["active_days"] / days_in_month * 100, 2
    )

    return MonthlyAnalyticsResponse(
        year=year,
        month=month,
        total_workouts=stats["total_workouts"],
        total_duration_minutes=stats["total_duration_minutes"],
        total_calories_burned=stats["total_calories_burned"],
        active_days=stats["active_days"],
        workout_consistency_percentage=consistency
    )


@router.get("/goals", response_model=GoalAnalyticsResponse)
def goal_analytics(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Connect your existing Goals model here.
    # Do not assume its status column or completion rules.
    raise HTTPException(
        status_code=501,
        detail="Connect this endpoint to the existing Goals model"
    )


@router.get("/insights", response_model=PerformanceInsights)
def performance_insights(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    today = date.today()

    start_date = today - timedelta(days=6)
    end_date = today + timedelta(days=1)

    stats = calculate_workout_stats(
        db,
        user.id,
        start_date,
        end_date
    )

    consistency = round(
        stats["active_days"] / 7 * 100, 2
    )

    insights = []

    if stats["total_workouts"] == 0:
        insights.append(
            "Start your first workout to build consistency."
        )
    elif consistency >= 70:
        insights.append(
            "Great consistency! Keep following your workout routine."
        )
    else:
        insights.append(
            "Try adding more active days to improve consistency."
        )

    return PerformanceInsights(
        total_workouts=stats["total_workouts"],
        total_calories_burned=stats["total_calories_burned"],
        total_workout_minutes=stats["total_duration_minutes"],
        current_streak=0,
        goal_completion_percentage=0,
        workout_consistency_percentage=consistency,
        insights=insights
    )
