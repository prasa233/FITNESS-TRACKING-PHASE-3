
import { useState } from "react";
import {
  LayoutDashboard,
  Apple,
  Droplets,
  Dumbbell,
  Timer,
  Link as LinkIcon,
  ChartNoAxesCombined,
  Bell,
  Menu,
  LogOut,
} from "lucide-react";
import Dashboard from "./pages/Dashboard";
import Nutrition from "./pages/Nutrition";
import WaterTracker from "./pages/WaterTracker";
import Recommendations from "./pages/Recommendations";
import WorkoutTimer from "./pages/WorkoutTimer";
import Integrations from "./pages/Integrations";
import Analytics from "./pages/Analytics";
import Reminders from "./pages/Reminders";

import { logout } from "./services/auth";
import { getToken } from "./services/auth";
import Auth from "./pages/Auth";

const navigation = [
  { name: "Dashboard", icon: LayoutDashboard },
  { name: "Nutrition", icon: Apple },
  { name: "Water Tracker", icon: Droplets },
  { name: "Recommendations", icon: Dumbbell },
  { name: "Workout Timer", icon: Timer },
  { name: "Integrations", icon: LinkIcon },
  { name: "Analytics", icon: ChartNoAxesCombined },
  { name: "Reminders", icon: Bell },
];

export default function App() {
  const [authenticated, setAuthenticated] = useState(Boolean(getToken()));
  const [active, setActive] = useState("Dashboard");
  const [menuOpen, setMenuOpen] = useState(false);

  if (!authenticated) {
    return <Auth onAuthenticated={() => setAuthenticated(true)} />;
  }

  const pages = {
    Dashboard: <Dashboard />,
    Nutrition: <Nutrition />,
    "Water Tracker": <WaterTracker />,
    Recommendations: <Recommendations />,
    "Workout Timer": <WorkoutTimer />,
    Integrations: <Integrations />,
    Analytics: <Analytics />,
    Reminders: <Reminders />,
  };

  return (
    <div className="app-layout">
      <aside className={`sidebar ${menuOpen ? "open" : ""}`}>
        <div className="brand">
          <div className="brand-icon">F</div>
          <div>
            <h2>FitTrack</h2>
            <small>SMART FITNESS</small>
          </div>
        </div>

        <p className="nav-heading">WORKSPACE</p>

        {navigation.map(({ name, icon: Icon }) => (
          <button
            key={name}
            className={`nav-item ${active === name ? "active" : ""}`}
            onClick={() => {
              setActive(name);
              setMenuOpen(false);
            }}
          >
            <Icon size={19} />
            <span>{name}</span>
          </button>
        ))}

        <div className="sidebar-bottom">
          <button className="nav-item" onClick={logout}>
            <LogOut size={19} />
            Logout
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <button
            className="menu-button"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <Menu />
          </button>

          <div>
            <h3>{active}</h3>
            <small>Your smart fitness companion</small>
          </div>

          <div className="profile">
            <div className="avatar">U</div>
            <span>User</span>
          </div>
        </header>

        <section className="page-content">
          {pages[active]}
        </section>
      </main>
    </div>
  );
}
