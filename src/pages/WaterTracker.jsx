
import { useEffect, useState } from "react";
import { Droplets, GlassWater } from "lucide-react";
import api from "../services/api";

export default function WaterTracker() {
  const [quantity, setQuantity] = useState(250);
  const [progress, setProgress] = useState({
    consumed_ml: 0,
    goal_ml: 3000,
    remaining_ml: 3000,
    progress_percentage: 0,
  });
  const [logs, setLogs] = useState([]);

  const loadWater = async () => {
    try {
      const [p, l] = await Promise.all([
        api.get("/phase3/water/daily-progress"),
        api.get("/phase3/water/logs"),
      ]);

      setProgress(p.data);
      setLogs(l.data);
    } catch (error) {
      console.error("Water loading failed:", error);
    }
  };

  useEffect(() => {
    loadWater();
  }, []);

  const addWater = async () => {
    try {
      await api.post("/phase3/water/log", {
        quantity: Number(quantity),
      });

      await loadWater();
    } catch (error) {
      alert(error.response?.data?.detail || "Unable to save water intake");
    }
  };

  const percentage = Math.min(
    progress.progress_percentage || 0,
    100
  );

  return (
    <div>
      <div className="page-title">
        <h2>Water Intake Tracker</h2>
        <p>Stay hydrated and achieve your daily water goal.</p>
      </div>

      <div className="panel water-panel">
        <Droplets size={35} />

        <h2>
          {(progress.consumed_ml / 1000).toFixed(2)} L
        </h2>

        <p>
          Daily Goal: {(progress.goal_ml / 1000).toFixed(1)} L
        </p>

        <div className="progress-track">
          <div
            className="progress-fill water-fill"
            style={{ width: `${percentage}%` }}
          />
        </div>

        <h3>{percentage.toFixed(1)}% Completed</h3>

        <p>
          Remaining: {(progress.remaining_ml / 1000).toFixed(2)} L
        </p>

        <div className="water-actions">
          <select
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
          >
            <option value="150">150 ml</option>
            <option value="250">250 ml</option>
            <option value="500">500 ml</option>
            <option value="750">750 ml</option>
            <option value="1000">1000 ml</option>
          </select>

          <button className="primary-button" onClick={addWater}>
            <GlassWater size={18} /> Add Water
          </button>
        </div>
      </div>

      <div className="panel">
        <h3>Water Intake History</h3>

        {logs.length === 0 ? (
          <p className="empty">No water intake recorded.</p>
        ) : (
          logs.map((log) => (
            <div className="meal-row" key={log.id}>
              <span>Water Intake</span>
              <strong>{log.quantity} ml</strong>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
