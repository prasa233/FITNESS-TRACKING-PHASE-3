
import { useEffect, useState } from "react";
import { Apple, Flame, Beef, Wheat, Trash2 } from "lucide-react";
import api from "../services/api";

export default function Nutrition() {
  const [meals, setMeals] = useState([]);
  const [summary, setSummary] = useState({
    total_calories: 0,
    total_protein: 0,
    total_carbs: 0,
    total_fats: 0,
    total_meals: 0,
  });

  const [form, setForm] = useState({
    meal_type: "Breakfast",
    food_name: "",
    calories: "",
    protein: "",
    carbs: "",
    fats: "",
  });

  const loadData = async () => {
    try {
      const [mealRes, summaryRes] = await Promise.all([
        api.get("/phase3/nutrition/meals"),
        api.get("/phase3/nutrition/summary"),
      ]);

      setMeals(mealRes.data);
      setSummary(summaryRes.data);
    } catch (error) {
      console.error("Nutrition loading failed:", error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.post("/phase3/nutrition/meals", {
        ...form,
        calories: Number(form.calories),
        protein: Number(form.protein),
        carbs: Number(form.carbs),
        fats: Number(form.fats),
      });

      alert("Meal added successfully!");

      setForm({
        meal_type: "Breakfast",
        food_name: "",
        calories: "",
        protein: "",
        carbs: "",
        fats: "",
      });

      loadData();
    } catch (error) {
      alert(error.response?.data?.detail || "Unable to add meal");
    }
  };

  const deleteMeal = async (id) => {
    try {
      await api.delete(`/phase3/nutrition/meals/${id}`);
      loadData();
    } catch (error) {
      alert("Unable to delete meal");
    }
  };

  const cards = [
    {
      title: "Calories",
      value: summary.total_calories,
      unit: "kcal",
      icon: Flame,
    },
    {
      title: "Protein",
      value: summary.total_protein,
      unit: "g",
      icon: Beef,
    },
    {
      title: "Carbohydrates",
      value: summary.total_carbs,
      unit: "g",
      icon: Wheat,
    },
    {
      title: "Fats",
      value: summary.total_fats,
      unit: "g",
      icon: Apple,
    },
  ];

  return (
    <div>
      <div className="page-title">
        <h2>Nutrition Tracking</h2>
        <p>Track your daily food intake and nutrition.</p>
      </div>

      <div className="stats-grid">
        {cards.map((card) => {
          const Icon = card.icon;

          return (
            <div className="stat-card" key={card.title}>
              <Icon size={23} />
              <p>{card.title}</p>
              <h2>
                {Number(card.value || 0).toFixed(1)}
                <small> {card.unit}</small>
              </h2>
            </div>
          );
        })}
      </div>

      <div className="content-grid">
        <div className="panel">
          <h3>Add Meal</h3>

          <form onSubmit={handleSubmit} className="form">
            <label>Meal Type</label>
            <select
              value={form.meal_type}
              onChange={(e) =>
                setForm({ ...form, meal_type: e.target.value })
              }
            >
              {["Breakfast", "Lunch", "Dinner", "Snacks"].map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>

            {[
              ["food_name", "Food Name", "text"],
              ["calories", "Calories", "number"],
              ["protein", "Protein (g)", "number"],
              ["carbs", "Carbohydrates (g)", "number"],
              ["fats", "Fats (g)", "number"],
            ].map(([key, label, type]) => (
              <div key={key}>
                <label>{label}</label>
                <input
                  type={type}
                  required
                  min={type === "number" ? "0" : undefined}
                  step={type === "number" ? "0.1" : undefined}
                  value={form[key]}
                  onChange={(e) =>
                    setForm({ ...form, [key]: e.target.value })
                  }
                />
              </div>
            ))}

            <button className="primary-button">
              Add Meal
            </button>
          </form>
        </div>

        <div className="panel">
          <h3>Today's Meals</h3>

          {meals.length === 0 ? (
            <p className="empty">No meals recorded yet.</p>
          ) : (
            meals.map((meal) => (
              <div className="meal-row" key={meal.id}>
                <div>
                  <strong>{meal.food_name}</strong>
                  <p>{meal.meal_type} · {meal.calories} kcal</p>
                </div>

                <button
                  className="icon-button danger"
                  onClick={() => deleteMeal(meal.id)}
                  aria-label="Delete meal"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
