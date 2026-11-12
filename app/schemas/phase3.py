
from datetime import date, datetime, time
from typing import Optional, Literal
from pydantic import BaseModel
from typing import Optional
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator
)


# ============================================================
# COMMON CONFIGURATION
# ============================================================

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ============================================================
# MODULE 13: NUTRITION & MEAL TRACKING
# ============================================================

class MealCreate(BaseModel):

    meal_type: Literal[
        "Breakfast",
        "Lunch",
        "Dinner",
        "Snacks"
    ]

    food_name: str = Field(
        min_length=1,
        max_length=150
    )

    calories: float = Field(
        ge=0,
        le=20000
    )

    protein: float = Field(
        default=0,
        ge=0,
        le=1000
    )

    carbs: float = Field(
        default=0,
        ge=0,
        le=1000
    )

    fats: float = Field(
        default=0,
        ge=0,
        le=1000
    )


class MealResponse(BaseResponse):

    id: int
    user_id: int
    meal_type: str
    food_name: str

    calories: float
    protein: float
    carbs: float
    fats: float

    created_at: datetime


class NutritionSummary(BaseModel):

    date: date

    total_calories: float = 0
    total_protein: float = 0
    total_carbs: float = 0
    total_fats: float = 0

    total_meals: int = 0


# ============================================================
# MODULE 14: WATER INTAKE TRACKER
# ============================================================

class WaterCreate(BaseModel):

    quantity: int = Field(
        gt=0,
        le=10000,
        description="Water quantity in milliliters"
    )


class WaterResponse(BaseResponse):

    id: int
    user_id: int
    quantity: int
    date: date

    created_at: Optional[datetime] = None


class WaterProgress(BaseModel):

    date: date

    consumed_ml: int = 0
    goal_ml: int = Field(gt=0)

    remaining_ml: int = 0

    progress_percentage: float = Field(
        ge=0,
        le=100
    )


# ============================================================
# MODULE 15: AI WORKOUT SUGGESTIONS
# ============================================================

class WorkoutRecommendationRequest(BaseModel):

    goal: Literal[
        "Weight Loss",
        "Muscle Gain",
        "Strength",
        "Fitness",
        "Endurance"
    ]

    fitness_level: Literal[
        "Beginner",
        "Intermediate",
        "Advanced"
    ] = "Beginner"

    available_minutes: int = Field(
        default=30,
        ge=5,
        le=300
    )

    equipment: list[str] = Field(
        default_factory=list,
        max_length=20
    )


class ExerciseSuggestion(BaseModel):

    exercise_name: str = Field(
        min_length=1,
        max_length=150
    )

    sets: int = Field(
        ge=1,
        le=20
    )

    repetitions: int = Field(
        ge=1,
        le=200
    )

    rest_seconds: int = Field(
        default=60,
        ge=0,
        le=600
    )


class WorkoutRecommendationResponse(BaseResponse):

    id: int
    user_id: int

    workout_name: str
    description: Optional[str] = None

    exercise_list: Optional[list[dict]] = None

    recommendation_reason: Optional[str] = None

    difficulty: str
    duration_minutes: int

    based_on: Optional[dict] = None

    is_completed: bool

    generated_at: datetime


class RecommendationCompletion(BaseModel):

    is_completed: bool


# ============================================================
# MODULE 16: WORKOUT TIMER & LIVE TRACKING
# ============================================================

class WorkoutStart(BaseModel):

    workout_name: str = Field(
        min_length=1,
        max_length=150
    )

    calories_per_minute: float = Field(
        default=5.0,
        gt=0,
        le=30
    )


class WorkoutStop(BaseModel):

    status: Literal[
        "COMPLETED",
        "CANCELLED"
    ] = "COMPLETED"


class WorkoutSessionResponse(BaseResponse):

    id: int
    user_id: int

    workout_name: str

    start_time: datetime
    end_time: Optional[datetime] = None

    duration_seconds: int
    calories_per_minute: float
    calories_burned: float

    status: str
    created_at: datetime


class WorkoutTimerStatus(BaseModel):

    session_id: int
    workout_name: str

    status: str

    start_time: datetime

    elapsed_seconds: int

    calories_burned: float


# ============================================================
# MODULE 17: THIRD-PARTY FITNESS INTEGRATION
# ============================================================




class FitnessIntegrationConnect(BaseModel):
    authorization_code: Optional[str] = None
    redirect_uri: Optional[str] = None


class FitnessIntegrationResponse(BaseResponse):
    id: int
    user_id: int
    provider: str
    scopes: Optional[list[str]] = None
    is_connected: bool
    last_synced_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class FitnessSyncRequest(BaseModel):
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def validate_date_range(cls, value, info):
        start_date = info.data.get("start_date")

        if start_date and value < start_date:
            raise ValueError(
                "End date cannot be earlier than start date"
            )

        return value


class SyncedActivityResponse(BaseResponse):
    id: int
    user_id: int
    integration_id: int
    external_activity_id: Optional[str] = None
    activity_type: str
    steps: int
    calories_burned: float
    duration_minutes: int
    activity_date: date
    synced_at: datetime


# ============================================================
# MODULE 18: ADVANCED ANALYTICS DASHBOARD
# ============================================================

class DailyWorkoutAnalytics(BaseModel):

    date: date

    workout_count: int = 0

    duration_minutes: int = 0

    calories_burned: float = 0


class WeeklyAnalyticsResponse(BaseModel):

    period: Literal["weekly"] = "weekly"

    start_date: date
    end_date: date

    total_workouts: int = 0

    total_duration_minutes: int = 0

    total_calories_burned: float = 0

    active_days: int = 0

    workout_consistency_percentage: float = Field(
        default=0,
        ge=0,
        le=100
    )

    daily_breakdown: list[DailyWorkoutAnalytics] = Field(
        default_factory=list
    )


class MonthlyAnalyticsResponse(BaseModel):

    period: Literal["monthly"] = "monthly"

    year: int = Field(ge=2000, le=2100)

    month: int = Field(ge=1, le=12)

    total_workouts: int = 0

    total_duration_minutes: int = 0

    total_calories_burned: float = 0

    active_days: int = 0

    workout_consistency_percentage: float = Field(
        default=0,
        ge=0,
        le=100
    )


class GoalAnalyticsResponse(BaseModel):

    total_goals: int = 0

    completed_goals: int = 0

    pending_goals: int = 0

    completion_percentage: float = Field(
        default=0,
        ge=0,
        le=100
    )


class PerformanceInsights(BaseModel):

    total_workouts: int = 0

    total_calories_burned: float = 0

    total_workout_minutes: int = 0

    current_streak: int = 0

    goal_completion_percentage: float = Field(
        default=0,
        ge=0,
        le=100
    )

    workout_consistency_percentage: float = Field(
        default=0,
        ge=0,
        le=100
    )

    insights: list[str] = Field(
        default_factory=list
    )


# ============================================================
# MODULE 19: IN-APP REMINDERS & ALERTS
# ============================================================

class ReminderCreate(BaseModel):

    reminder_type: Literal[
        "Workout",
        "Meal",
        "Water"
    ]

    title: str = Field(
        min_length=1,
        max_length=150
    )

    message: Optional[str] = Field(
        default=None,
        max_length=1000
    )

    reminder_time: time

    timezone: str = Field(
        default="Asia/Kolkata",
        min_length=1,
        max_length=50
    )

    repeat_days: list[int] = Field(
        default_factory=list,
        max_length=7
    )

    is_active: bool = True

    @field_validator("repeat_days")
    @classmethod
    def validate_repeat_days(cls, value):
        if any(day < 0 or day > 6 for day in value):
            raise ValueError(
                "Repeat days must be between 0 and 6"
            )

        if len(value) != len(set(value)):
            raise ValueError(
                "Repeat days cannot contain duplicates"
            )

        return value


class ReminderUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=150
    )

    message: Optional[str] = Field(
        default=None,
        max_length=1000
    )

    reminder_time: Optional[time] = None

    timezone: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    repeat_days: Optional[list[int]] = Field(
        default=None,
        max_length=7
    )

    is_active: Optional[bool] = None

    @field_validator("repeat_days")
    @classmethod
    def validate_repeat_days(cls, value):
        if value is None:
            return value

        if any(day < 0 or day > 6 for day in value):
            raise ValueError(
                "Repeat days must be between 0 and 6"
            )

        if len(value) != len(set(value)):
            raise ValueError(
                "Repeat days cannot contain duplicates"
            )

        return value


class ReminderResponse(BaseResponse):

    id: int
    user_id: int

    reminder_type: str

    title: str
    message: Optional[str] = None

    reminder_time: str

    timezone: Optional[str] = None

    repeat_days: Optional[list[int]] = None

    next_run_at: Optional[datetime] = None

    is_active: bool

    last_sent_at: Optional[datetime] = None

    created_at: datetime


class ReminderLogResponse(BaseResponse):

    id: int

    reminder_id: int
    user_id: int

    message: str

    delivery_status: str

    sent_at: Optional[datetime] = None

    created_at: datetime
