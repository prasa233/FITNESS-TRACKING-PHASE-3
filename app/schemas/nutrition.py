
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class MealCreate(BaseModel):
    meal_type: Literal[
        "Breakfast",
        "Lunch",
        "Dinner",
        "Snacks"
    ]

    food_name: str = Field(min_length=2, max_length=150)

    calories: float = Field(ge=0, le=10000)
    protein: float = Field(ge=0, le=1000)
    carbs: float = Field(ge=0, le=1000)
    fats: float = Field(ge=0, le=1000)


class MealResponse(BaseModel):
    id: int
    user_id: int
    meal_type: str
    food_name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NutritionSummary(BaseModel):
    date: str
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float
    total_meals: int
