
from app.schemas.phase3 import (
    MealCreate,
    WaterCreate,
    WorkoutStart,
    ReminderCreate
)

# Test Module 13
meal = MealCreate(
    meal_type="Breakfast",
    food_name="Oats and Milk",
    calories=250,
    protein=12,
    carbs=35,
    fats=7
)

print("MEAL VALIDATION:")
print(meal.model_dump())

# Test Module 14
water = WaterCreate(
    quantity=500
)

print("\nWATER VALIDATION:")
print(water.model_dump())

# Test Module 16
workout = WorkoutStart(
    workout_name="Morning Cardio",
    calories_per_minute=5
)

print("\nWORKOUT VALIDATION:")
print(workout.model_dump())

# Test Module 19
reminder = ReminderCreate(
    reminder_type="Water",
    title="Drink Water",
    message="Drink 500ml water",
    reminder_time="08:30",
    timezone="Asia/Kolkata",
    repeat_days=[0, 1, 2, 3, 4, 5, 6]
)

print("\nREMINDER VALIDATION:")
print(reminder.model_dump())

print("\nALL SCHEMA TESTS PASSED")