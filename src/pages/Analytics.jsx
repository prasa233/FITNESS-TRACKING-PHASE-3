
import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

import api from "../services/api";

export default function Analytics() {
  const [weekly, setWeekly] = useState(null);
  const [monthly, setMonthly] = useState(null);
  const [insights, setInsights] = useState(null);

  const loadAnalytics = async () => {
    try {
      const [w, m, i] = await Promise.all([
        api.get("/phase3/analytics/weekly"),
        api.get("/phase3/analytics/monthly"),
        api.get("/phase3/analytics/insights"),
      ]);

      setWeekly(w.data);
      setMonthly(m.data);
      setInsights(i.data);
    } catch (error) {
      console.error("Analytics loading failed:", error);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  return (
    <div>
      <div className="page-title">
        <h2>Advanced Analytics</h2>
        <p>Understand your fitness performance and progress.</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Weekly Workouts</h3>
          <h2>{weekly?.total_workouts ?? 0}</h2>
        </div>

        <div className="stat-card">
          <h3>Calories Burned</h3>
          <h2>{weekly?.total_calories_burned ?? 0}</h2>
        </div>

        <div className="stat-card">
          <h3>Active Days</h3>
          <h2>{weekly?.active_days ?? 0}</h2>
        </div>

        <div className="stat-card">
          <h3>Consistency</h3>
          <h2>
            {weekly?.workout_consistency_percentage ?? 0}%
          </h2>
        </div>
      </div>

      <div className="panel">
        <h3>Weekly Performance</h3>

        <div className="chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weekly?.daily_breakdown || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="calories_burned" name="Calories Burned" />
              <Bar dataKey="duration_minutes" name="Minutes" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="panel">
        <h3>Monthly Performance</h3>

        <div className="stats-grid">
          <div>
            <p>Total Workouts</p>
            <h2>{monthly?.total_workouts ?? 0}</h2>
          </div>

          <div>
            <p>Workout Minutes</p>
            <h2>{monthly?.total_duration_minutes ?? 0}</h2>
          </div>

          <div>
            <p>Consistency</p>
            <h2>
              {monthly?.workout_consistency_percentage ?? 0}%
            </h2>
          </div>
        </div>
      </div>

      <div className="panel">
        <h3>Performance Insights</h3>

        {(insights?.insights || []).map((item, index) => (
          <p key={index}>• {item}</p>
        ))}

        {!insights && <p>Loading performance insights...</p>}
      </div>
    </div>
  );
}
