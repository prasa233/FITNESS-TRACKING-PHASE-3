
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime, timezone

from app.core.database import Base


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    meal_type = Column(String(20), nullable=False)
    food_name = Column(String(150), nullable=False)

    calories = Column(Float, nullable=False, default=0)
    protein = Column(Float, nullable=False, default=0)
    carbs = Column(Float, nullable=False, default=0)
    fats = Column(Float, nullable=False, default=0)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False
    )
