
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.phase3 import Meal
from app.schemas.phase3 import MealCreate, MealResponse, NutritionSummary


router = APIRouter(
    prefix="/phase3/nutrition",
    tags=["Nutrition"]
)


@router.post("/meals", response_model=MealResponse, status_code=201)
def add_meal(
    data: MealCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    meal = Meal(
        user_id=user.id,
        **data.model_dump()
    )

    db.add(meal)
    db.commit()
    db.refresh(meal)

    return meal


@router.get("/meals", response_model=list[MealResponse])
def get_meals(
    selected_date: date | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Meal).filter(
        Meal.user_id == user.id
    )

    if selected_date:
        query = query.filter(
            func.date(Meal.created_at) == selected_date.isoformat()
        )

    return query.order_by(Meal.created_at.desc()).all()


@router.get("/meals/{meal_id}", response_model=MealResponse)
def get_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    meal = db.query(Meal).filter(
        Meal.id == meal_id,
        Meal.user_id == user.id
    ).first()

    if not meal:
        raise HTTPException(404, "Meal not found")

    return meal


@router.put("/meals/{meal_id}", response_model=MealResponse)
def update_meal(
    meal_id: int,
    data: MealCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    meal = db.query(Meal).filter(
        Meal.id == meal_id,
        Meal.user_id == user.id
    ).first()

    if not meal:
        raise HTTPException(404, "Meal not found")

    for key, value in data.model_dump().items():
        setattr(meal, key, value)

    db.commit()
    db.refresh(meal)

    return meal


@router.delete("/meals/{meal_id}")
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    meal = db.query(Meal).filter(
        Meal.id == meal_id,
        Meal.user_id == user.id
    ).first()

    if not meal:
        raise HTTPException(404, "Meal not found")

    db.delete(meal)
    db.commit()

    return {"message": "Meal deleted successfully"}


@router.get("/summary", response_model=NutritionSummary)
def nutrition_summary(
    selected_date: date | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    selected_date = selected_date or date.today()

    result = db.query(
        func.coalesce(func.sum(Meal.calories), 0),
        func.coalesce(func.sum(Meal.protein), 0),
        func.coalesce(func.sum(Meal.carbs), 0),
        func.coalesce(func.sum(Meal.fats), 0),
        func.count(Meal.id)
    ).filter(
        Meal.user_id == user.id,
        func.date(Meal.created_at) == selected_date.isoformat()
    ).first()

    return NutritionSummary(
        date=selected_date,
        total_calories=result[0],
        total_protein=result[1],
        total_carbs=result[2],
        total_fats=result[3],
        total_meals=result[4]
    )
