

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
    JSON,
    CheckConstraint,
    UniqueConstraint,
    Index
)
from sqlalchemy.sql import func

from app.core.database import Base


# =====================================================
# MODULE 13: NUTRITION & MEAL TRACKING
# =====================================================

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    meal_type = Column(String(30), nullable=False)
    food_name = Column(String(150), nullable=False)

    calories = Column(Float, nullable=False, default=0)
    protein = Column(Float, nullable=False, default=0)
    carbs = Column(Float, nullable=False, default=0)
    fats = Column(Float, nullable=False, default=0)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "meal_type IN ('Breakfast', 'Lunch', 'Dinner', 'Snacks')",
            name="check_meal_type"
        ),
        CheckConstraint(
            "calories >= 0 AND protein >= 0 AND carbs >= 0 AND fats >= 0",
            name="check_meal_nutrition"
        ),
        Index("idx_meals_user_created", "user_id", "created_at"),
    )


# =====================================================
# MODULE 14: WATER INTAKE TRACKER
# =====================================================

class WaterTracking(Base):
    __tablename__ = "water_tracking"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    quantity = Column(Integer, nullable=False)

    date = Column(Date, nullable=False, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="check_water_quantity"
        ),
        Index("idx_water_user_date", "user_id", "date"),
    )


# =====================================================
# MODULE 15: AI WORKOUT SUGGESTIONS
# =====================================================

class WorkoutRecommendation(Base):
    __tablename__ = "workout_recommendations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    workout_name = Column(String(150), nullable=False)

    description = Column(Text, nullable=True)

    exercise_list = Column(JSON, nullable=True)

    recommendation_reason = Column(Text, nullable=True)

    difficulty = Column(String(30), default="Beginner")

    duration_minutes = Column(Integer, default=30)

    based_on = Column(JSON, nullable=True)

    is_completed = Column(Boolean, default=False)

    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "difficulty IN ('Beginner', 'Intermediate', 'Advanced')",
            name="check_recommendation_difficulty"
        ),
    )


# =====================================================
# MODULE 16: WORKOUT TIMER & LIVE TRACKING
# =====================================================

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    workout_name = Column(String(150), nullable=False)

    start_time = Column(
        DateTime(timezone=True),
        nullable=False
    )

    end_time = Column(
        DateTime(timezone=True),
        nullable=True
    )

    duration_seconds = Column(Integer, default=0)

    calories_per_minute = Column(Float, default=5.0)

    calories_burned = Column(Float, default=0)

    status = Column(
        String(30),
        default="IN_PROGRESS",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('IN_PROGRESS', 'COMPLETED', 'CANCELLED')",
            name="check_workout_session_status"
        ),
        CheckConstraint(
            "duration_seconds >= 0 AND calories_burned >= 0",
            name="check_workout_session_values"
        ),
    )


# =====================================================
# MODULE 17: THIRD-PARTY INTEGRATIONS
# =====================================================

class FitnessIntegration(Base):
    __tablename__ = "fitness_integrations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    provider = Column(
        String(50),
        nullable=False
    )

    access_token_encrypted = Column(Text, nullable=True)

    refresh_token_encrypted = Column(Text, nullable=True)

    token_expires_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    scopes = Column(JSON, nullable=True)

    is_connected = Column(Boolean, default=False)

    last_synced_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "provider IN ('GOOGLE_FIT', 'APPLE_HEALTH')",
            name="check_fitness_provider"
        ),
        UniqueConstraint(
            "user_id",
            "provider",
            name="unique_user_fitness_provider"
        ),
    )


class SyncedActivity(Base):
    __tablename__ = "synced_activities"

    id = Column(Integer, primary_key=True, index=True)
    distance = Column(Float, nullable=False, default=0.0)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    integration_id = Column(
        Integer,
        ForeignKey("fitness_integrations.id"),
        nullable=False
    )

    external_activity_id = Column(String(150), nullable=True)

    activity_type = Column(String(100), nullable=False)

    steps = Column(Integer, default=0)

    calories_burned = Column(Float, default=0)

    duration_minutes = Column(Integer, default=0)

    activity_date = Column(Date, nullable=False)

    synced_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "steps >= 0 AND calories_burned >= 0 AND duration_minutes >= 0",
            name="check_synced_activity_values"
        ),
        UniqueConstraint(
            "integration_id",
            "external_activity_id",
            name="unique_external_activity"
        ),
    )


# =====================================================
# MODULE 18: ADVANCED ANALYTICS
# =====================================================

# Analytics are calculated from existing data:
# - meals
# - water_tracking
# - workout_sessions
# - workouts
# - goals
# - streak
#
# We do not need a separate analytics table
# for weekly and monthly calculations.


# =====================================================
# MODULE 19: IN-APP REMINDERS & ALERTS
# =====================================================

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    reminder_type = Column(
        String(30),
        nullable=False
    )

    title = Column(String(150), nullable=False)

    message = Column(Text, nullable=True)

    reminder_time = Column(
        String(5),
        nullable=False
    )

    timezone = Column(
        String(50),
        default="Asia/Kolkata"
    )

    repeat_days = Column(JSON, nullable=True)

    next_run_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    is_active = Column(Boolean, default=True)

    last_sent_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "reminder_type IN ('Workout', 'Meal', 'Water')",
            name="check_reminder_type"
        ),
    )


class ReminderLog(Base):
    __tablename__ = "reminder_logs"

    id = Column(Integer, primary_key=True, index=True)

    reminder_id = Column(
        Integer,
        ForeignKey("reminders.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    message = Column(Text, nullable=False)

    delivery_status = Column(
        String(30),
        default="PENDING"
    )

    sent_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
