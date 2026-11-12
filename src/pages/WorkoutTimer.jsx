
import { useEffect, useState } from "react";
import { Timer, Play, Square } from "lucide-react";
import api from "../services/api";

export default function WorkoutTimer() {
  const [workoutName, setWorkoutName] = useState("Morning Cardio");
  const [caloriesPerMinute, setCaloriesPerMinute] = useState(5);
  const [session, setSession] = useState(null);
  const [elapsed, setElapsed] = useState(0);
  const [history, setHistory] = useState([]);

  const loadHistory = async () => {
    try {
      const response = await api.get("/phase3/timer/history");
      setHistory(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const loadActive = async () => {
    try {
      const response = await api.get("/phase3/timer/active");
      setSession(response.data);
      setElapsed(response.data.elapsed_seconds);
    } catch {
      setSession(null);
      setElapsed(0);
    }
  };

  useEffect(() => {
    loadActive();
    loadHistory();
  }, []);

  useEffect(() => {
    if (!session) return;

    const interval = setInterval(() => {
      setElapsed((value) => value + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [session?.session_id]);

  const startWorkout = async () => {
    try {
      const response = await api.post("/phase3/timer/start", {
        workout_name: workoutName,
        calories_per_minute: Number(caloriesPerMinute),
      });

      setSession(response.data);
      setElapsed(0);
    } catch (error) {
      alert(error.response?.data?.detail || "Unable to start workout");
    }
  };

  const stopWorkout = async () => {
    try {
      await api.post(
        `/phase3/timer/${session.id || session.session_id}/stop`,
        { status: "COMPLETED" }
      );

      setSession(null);
      setElapsed(0);

      await loadHistory();
    } catch (error) {
      alert(error.response?.data?.detail || "Unable to stop workout");
    }
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    return [hours, minutes, secs]
      .map((n) => String(n).padStart(2, "0"))
      .join(":");
  };

  return (
    <div>
      <div className="page-title">
        <h2>Workout Timer</h2>
        <p>Track your exercise duration in real time.</p>
      </div>

      <div className="panel timer-panel">
        <Timer size={40} />

        <h1 className="timer-display">
          {formatTime(elapsed)}
        </h1>

        <p>
          {session
            ? session.workout_name
            : "Ready to start your workout?"}
        </p>

        {!session && (
          <div className="form timer-form">
            <label>Workout Name</label>
            <input
              value={workoutName}
              onChange={(e) => setWorkoutName(e.target.value)}
            />

            <label>Estimated Calories Per Minute</label>
            <input
              type="number"
              min="0.1"
              step="0.1"
              value={caloriesPerMinute}
              onChange={(e) => setCaloriesPerMinute(e.target.value)}
            />

            <button className="primary-button" onClick={startWorkout}>
              <Play size={18} /> Start Workout
            </button>
          </div>
        )}

        {session && (
          <>
            <h3>
              Estimated Calories:{" "}
              {(
                elapsed / 60 * (session.calories_per_minute || 5)
              ).toFixed(1)} kcal
            </h3>

            <button className="danger-button" onClick={stopWorkout}>
              <Square size={18} /> Stop Workout
            </button>
          </>
        )}
      </div>

      <div className="panel">
        <h3>Workout History</h3>

        {history.map((item) => (
          <div className="meal-row" key={item.id}>
            <div>
              <strong>{item.workout_name}</strong>
              <p>{item.status}</p>
            </div>
            <strong>
              {Math.round((item.duration_seconds || 0) / 60)} min
            </strong>
          </div>
        ))}
      </div>
    </div>
  );
}
