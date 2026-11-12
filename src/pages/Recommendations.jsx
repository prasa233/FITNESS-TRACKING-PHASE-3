
import { useState } from "react";
import { Dumbbell, Sparkles } from "lucide-react";
import api from "../services/api";

export default function Recommendations() {
  const [form, setForm] = useState({
    goal: "Weight Loss",
    fitness_level: "Beginner",
    available_minutes: 30,
    equipment: [],
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const generate = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await api.post(
        "/phase3/recommendations/generate",
        {
          ...form,
          available_minutes: Number(form.available_minutes),
        }
      );

      setResult(response.data);
    } catch (error) {
      alert(
        error.response?.data?.detail ||
        "Unable to generate recommendation"
      );
    } finally {
      setLoading(false);
    }
  };

  const complete = async () => {
    try {
      await api.patch(
        `/phase3/recommendations/${result.id}/complete`
      );

      setResult({ ...result, is_completed: true });
    } catch (error) {
      alert("Unable to update workout");
    }
  };

  return (
    <div>
      <div className="page-title">
        <h2>AI Workout Suggestions</h2>
        <p>Discover workouts based on your fitness goals.</p>
      </div>

      <div className="panel">
        <h3><Sparkles size={20} /> Generate Recommendation</h3>

        <form onSubmit={generate} className="form">
          <label>Fitness Goal</label>
          <select
            value={form.goal}
            onChange={(e) =>
              setForm({ ...form, goal: e.target.value })
            }
          >
            {[
              "Weight Loss",
              "Muscle Gain",
              "Strength",
              "Fitness",
              "Endurance",
            ].map((goal) => (
              <option key={goal}>{goal}</option>
            ))}
          </select>

          <label>Fitness Level</label>
          <select
            value={form.fitness_level}
            onChange={(e) =>
              setForm({ ...form, fitness_level: e.target.value })
            }
          >
            <option>Beginner</option>
            <option>Intermediate</option>
            <option>Advanced</option>
          </select>

          <label>Available Minutes</label>
          <input
            type="number"
            min="5"
            max="300"
            value={form.available_minutes}
            onChange={(e) =>
              setForm({
                ...form,
                available_minutes: e.target.value,
              })
            }
          />

          <label>Equipment</label>
          <input
            placeholder="Example: Yoga Mat, Dumbbells"
            onChange={(e) =>
              setForm({
                ...form,
                equipment: e.target.value
                  .split(",")
                  .map((item) => item.trim())
                  .filter(Boolean),
              })
            }
          />

          <button className="primary-button" disabled={loading}>
            <Sparkles size={18} />
            {loading ? "Generating..." : "Generate Workout"}
          </button>
        </form>
      </div>

      {result && (
        <div className="panel recommendation-card">
          <Dumbbell size={30} />

          <h2>{result.workout_name}</h2>
          <p>{result.description}</p>

          <p>
            Difficulty: <strong>{result.difficulty}</strong>
          </p>
          <p>
            Duration: <strong>{result.duration_minutes} minutes</strong>
          </p>

          <h3>Recommended Exercises</h3>

          {(result.exercise_list || []).map((exercise, index) => (
            <div className="meal-row" key={index}>
              <div>
                <strong>{exercise.exercise_name}</strong>
                <p>
                  {exercise.sets} sets × {exercise.repetitions} reps
                </p>
              </div>
            </div>
          ))}

          <p>{result.recommendation_reason}</p>

          <button
            className="primary-button"
            onClick={complete}
            disabled={result.is_completed}
          >
            {result.is_completed ? "Completed" : "Mark as Completed"}
          </button>
        </div>
      )}
    </div>
  );
}
