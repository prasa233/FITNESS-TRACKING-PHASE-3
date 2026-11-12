
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.phase3 import (
    WorkoutRecommendation,
    WorkoutSession
)

from app.schemas.phase3 import (
    WorkoutRecommendationRequest,
    WorkoutRecommendationResponse
)


router = APIRouter(
    prefix="/phase3/recommendations",
    tags=["AI Workout Suggestions"]
)


WORKOUT_LIBRARY = {
    "Weight Loss": [
        {
            "name": "Fat Burning Cardio",
            "exercises": [
                {"exercise_name": "Jumping Jacks", "sets": 3,
                 "repetitions": 20, "rest_seconds": 45},
                {"exercise_name": "Squats", "sets": 3,
                 "repetitions": 15, "rest_seconds": 60},
                {"exercise_name": "Mountain Climbers", "sets": 3,
                 "repetitions": 20, "rest_seconds": 45}
            ]
        }
    ],
    "Muscle Gain": [
        {
            "name": "Muscle Building Workout",
            "exercises": [
                {"exercise_name": "Push Ups", "sets": 3,
                 "repetitions": 12, "rest_seconds": 60},
                {"exercise_name": "Dumbbell Curls", "sets": 3,
                 "repetitions": 12, "rest_seconds": 60},
                {"exercise_name": "Squats", "sets": 3,
                 "repetitions": 15, "rest_seconds": 60}
            ]
        }
    ],
    "Strength": [
        {
            "name": "Strength Training",
            "exercises": [
                {"exercise_name": "Squats", "sets": 4,
                 "repetitions": 10, "rest_seconds": 90},
                {"exercise_name": "Push Ups", "sets": 4,
                 "repetitions": 10, "rest_seconds": 60}
            ]
        }
    ],
    "Fitness": [
        {
            "name": "Full Body Fitness",
            "exercises": [
                {"exercise_name": "Squats", "sets": 3,
                 "repetitions": 15, "rest_seconds": 45},
                {"exercise_name": "Plank", "sets": 3,
                 "repetitions": 30, "rest_seconds": 45}
            ]
        }
    ],
    "Endurance": [
        {
            "name": "Endurance Training",
            "exercises": [
                {"exercise_name": "Jogging", "sets": 1,
                 "repetitions": 1, "rest_seconds": 60},
                {"exercise_name": "Jumping Jacks", "sets": 3,
                 "repetitions": 25, "rest_seconds": 45}
            ]
        }
    ]
}


@router.post(
    "/generate",
    response_model=WorkoutRecommendationResponse
)
def generate_recommendation(
    data: WorkoutRecommendationRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    history = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user.id,
        WorkoutSession.status == "COMPLETED"
    ).order_by(
        WorkoutSession.start_time.desc()
    ).limit(10).all()

    template = WORKOUT_LIBRARY[data.goal][0]

    completed_count = len(history)

    description = (
        f"{data.fitness_level} workout designed for "
        f"{data.goal}. Equipment: "
        f"{', '.join(data.equipment) if data.equipment else 'No equipment'}."
    )

    reason = (
        f"Selected for your {data.goal} goal and "
        f"{data.fitness_level} fitness level. "
        f"Previous completed workouts considered: {completed_count}."
    )

    recommendation = WorkoutRecommendation(
        user_id=user.id,
        workout_name=template["name"],
        description=description,
        exercise_list=template["exercises"],
        recommendation_reason=reason,
        difficulty=data.fitness_level,
        duration_minutes=data.available_minutes,
        based_on={
            "goal": data.goal,
            "fitness_level": data.fitness_level,
            "available_minutes": data.available_minutes,
            "equipment": data.equipment,
            "previous_workouts": completed_count
        },
        is_completed=False
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation


@router.get(
    "/",
    response_model=list[WorkoutRecommendationResponse]
)
def get_recommendations(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(WorkoutRecommendation).filter(
        WorkoutRecommendation.user_id == user.id
    ).order_by(
        WorkoutRecommendation.generated_at.desc()
    ).all()


@router.patch("/{recommendation_id}/complete")
def complete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    recommendation = db.query(
        WorkoutRecommendation
    ).filter(
        WorkoutRecommendation.id == recommendation_id,
        WorkoutRecommendation.user_id == user.id
    ).first()

    if not recommendation:
        from fastapi import HTTPException
        raise HTTPException(404, "Recommendation not found")

    recommendation.is_completed = True

    db.commit()

    return {
        "message": "Recommendation completed successfully"
    }
