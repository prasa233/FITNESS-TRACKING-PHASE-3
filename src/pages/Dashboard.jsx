
import React from "react";
import {
  Flame,
  Droplets,
  Dumbbell,
  Activity,
  Bell,
  Search,
  ArrowUpRight,
  Target,
  Utensils,
  Clock,
  TrendingUp
} from "lucide-react";
import "./Dashboard.css";

const stats = [
  {
    title: "Calories Consumed",
    value: "1,530",
    unit: "kcal",
    target: "Target: 2,200 kcal",
    percent: 70,
    icon: Flame,
    color: "orange"
  },
  {
    title: "Water Consumed",
    value: "1.25",
    unit: "liters",
    target: "Goal: 3 liters",
    percent: 42,
    icon: Droplets,
    color: "blue"
  },
  {
    title: "Weekly Workouts",
    value: "0",
    unit: "workouts",
    target: "Goal: 5 workouts",
    percent: 0,
    icon: Dumbbell,
    color: "purple"
  },
  {
    title: "Calories Burned",
    value: "0",
    unit: "kcal",
    target: "Daily activity",
    percent: 0,
    icon: Activity,
    color: "green"
  }
];

const nutrition = [
  { name: "Protein", amount: "105 g", percent: 70, color: "protein" },
  { name: "Carbohydrates", amount: "165 g", percent: 65, color: "carbs" },
  { name: "Fats", amount: "48 g", percent: 55, color: "fats" }
];

export default function Dashboard() {
  return (
    <div className="fit-dashboard">

      <header className="dashboard-header">
        <div>
          <span className="eyebrow">FITNESS OVERVIEW</span>
          <h1>Dashboard</h1>
          <p>Your smart fitness companion</p>
        </div>

        <div className="header-actions">
          <button className="icon-button">
            <Search size={19} />
          </button>
          <button className="icon-button">
            <Bell size={19} />
          </button>
          <div className="user-profile">
            <div className="avatar">U</div>
            <div>
              <strong>User</strong>
              <span>Fitness Member</span>
            </div>
          </div>
        </div>
      </header>

      <section className="welcome-banner">
        <div className="welcome-content">
          <span className="welcome-label">YOUR FITNESS JOURNEY</span>
          <h2>Welcome to FitTrack! 👋</h2>
          <p>
            Every small step brings you closer to a healthier,
            stronger you. Keep moving forward!
          </p>
          <button className="welcome-button">
            Explore Your Progress
            <ArrowUpRight size={17} />
          </button>
        </div>

        <div className="welcome-decoration">
          <Activity size={110} strokeWidth={1.2} />
        </div>
      </section>

      <section className="stats-grid">
        {stats.map((item) => {
          const Icon = item.icon;

          return (
            <div className="stat-card" key={item.title}>
              <div className={`stat-icon ${item.color}`}>
                <Icon size={23} />
              </div>

              <p className="stat-title">{item.title}</p>

              <div className="stat-value">
                {item.value}
                <span>{item.unit}</span>
              </div>

              <div className="stat-progress">
                <div
                  className={`progress-fill ${item.color}`}
                  style={{ width: `${item.percent}%` }}
                />
              </div>

              <span className="stat-target">{item.target}</span>
            </div>
          );
        })}
      </section>

      <section className="dashboard-content-grid">

        <div className="dashboard-panel nutrition-panel">
          <div className="panel-heading">
            <div>
              <span className="panel-subtitle">NUTRITION TRACKING</span>
              <h3>Daily Nutrition</h3>
            </div>
            <div className="panel-icon orange">
              <Utensils size={20} />
            </div>
          </div>

          <div className="calorie-overview">
            <div>
              <h2>1,530 <span>kcal</span></h2>
              <p>Today's calorie intake</p>
            </div>
            <div className="calorie-goal">
              <Target size={17} />
              <span>Goal: 2,200</span>
            </div>
          </div>

          <div className="nutrition-list">
            {nutrition.map((item) => (
              <div className="nutrition-item" key={item.name}>
                <div className="nutrition-info">
                  <span>{item.name}</span>
                  <strong>{item.amount}</strong>
                </div>

                <div className="nutrition-track">
                  <div
                    className={`nutrition-fill ${item.color}`}
                    style={{ width: `${item.percent}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="dashboard-panel hydration-panel">
          <div className="panel-heading">
            <div>
              <span className="panel-subtitle">DAILY HYDRATION</span>
              <h3>Water Tracker</h3>
            </div>
            <div className="panel-icon blue">
              <Droplets size={20} />
            </div>
          </div>

          <div className="hydration-content">
            <div className="hydration-circle">
              <div className="hydration-inner">
                <Droplets size={23} />
                <strong>41.77%</strong>
                <span>Completed</span>
              </div>
            </div>

            <div className="water-details">
              <h2>1,253 <span>ml</span></h2>
              <p>of 3,000 ml daily goal</p>
              <div className="water-remaining">
                1,747 ml remaining
              </div>
            </div>
          </div>
        </div>

      </section>

      <section className="dashboard-panel weekly-panel">
        <div className="panel-heading">
          <div>
            <span className="panel-subtitle">ACTIVITY OVERVIEW</span>
            <h3>Weekly Fitness Summary</h3>
          </div>
          <div className="panel-icon purple">
            <TrendingUp size={20} />
          </div>
        </div>

        <div className="weekly-summary">
          <div className="weekly-main">
            <h2>0 <span>minutes</span></h2>
            <p>Total workout duration this week</p>
          </div>

          <div className="weekly-details">
            <div>
              <Dumbbell size={19} />
              <span>Workouts</span>
              <strong>0</strong>
            </div>
            <div>
              <Flame size={19} />
              <span>Calories burned</span>
              <strong>0 kcal</strong>
            </div>
            <div>
              <Clock size={19} />
              <span>Active time</span>
              <strong>0 min</strong>
            </div>
          </div>
        </div>

        <div className="weekly-days">
          {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map(day => (
            <div className="day-item" key={day}>
              <div className="day-bar">
                <div />
              </div>
              <span>{day}</span>
            </div>
          ))}
        </div>
      </section>

      <footer className="dashboard-footer">
        <span>© 2026 FitTrack Smart Fitness</span>
        <span>Stay healthy. Stay consistent. 💚</span>
      </footer>

    </div>
  );
}
