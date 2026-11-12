
import { useEffect, useState } from "react";
import { Bell, Trash2 } from "lucide-react";
import api from "../services/api";

export default function Reminders() {
  const [reminders, setReminders] = useState([]);

  const [form, setForm] = useState({
    reminder_type: "Water",
    title: "",
    message: "",
    reminder_time: "08:30:00",
    timezone: "Asia/Kolkata",
    repeat_days: [0, 1, 2, 3, 4, 5, 6],
    is_active: true,
  });

  const loadReminders = async () => {
    try {
      const response = await api.get("/phase3/reminders/");
      setReminders(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadReminders();
  }, []);

  const createReminder = async (e) => {
    e.preventDefault();

    try {
      await api.post("/phase3/reminders/", form);

      alert("Reminder created successfully!");

      setForm({
        ...form,
        title: "",
        message: "",
      });

      loadReminders();
    } catch (error) {
      alert(error.response?.data?.detail || "Unable to create reminder");
    }
  };

  const toggleReminder = async (id) => {
    try {
      await api.patch(`/phase3/reminders/${id}/toggle`);
      loadReminders();
    } catch (error) {
      alert("Unable to update reminder");
    }
  };

  const deleteReminder = async (id) => {
    try {
      await api.delete(`/phase3/reminders/${id}`);
      loadReminders();
    } catch (error) {
      alert("Unable to delete reminder");
    }
  };

  return (
    <div>
      <div className="page-title">
        <h2>Reminders & Alerts</h2>
        <p>Build healthy habits with daily reminders.</p>
      </div>

      <div className="panel">
        <h3><Bell size={20} /> Create Reminder</h3>

        <form className="form" onSubmit={createReminder}>
          <label>Reminder Type</label>

          <select
            value={form.reminder_type}
            onChange={(e) =>
              setForm({ ...form, reminder_type: e.target.value })
            }
          >
            <option>Water</option>
            <option>Meal</option>
            <option>Workout</option>
          </select>

          <label>Title</label>
          <input
            required
            value={form.title}
            onChange={(e) =>
              setForm({ ...form, title: e.target.value })
            }
          />

          <label>Message</label>
          <input
            required
            value={form.message}
            onChange={(e) =>
              setForm({ ...form, message: e.target.value })
            }
          />

          <label>Reminder Time</label>
          <input
            type="time"
            required
            value={form.reminder_time.slice(0, 5)}
            onChange={(e) =>
              setForm({
                ...form,
                reminder_time: e.target.value + ":00",
              })
            }
          />

          <button className="primary-button">
            Create Reminder
          </button>
        </form>
      </div>

      <div className="panel">
        <h3>My Reminders</h3>

        {reminders.length === 0 && (
          <p className="empty">No reminders created yet.</p>
        )}

        {reminders.map((item) => (
          <div className="meal-row" key={item.id}>
            <div>
              <strong>{item.title}</strong>
              <p>
                {item.reminder_type} · {item.reminder_time}
              </p>
              <span className="status-badge">
                {item.is_active ? "Active" : "Inactive"}
              </span>
            </div>

            <div className="row-actions">
              <button
                className="secondary-button"
                onClick={() => toggleReminder(item.id)}
              >
                {item.is_active ? "Disable" : "Enable"}
              </button>

              <button
                className="icon-button danger"
                onClick={() => deleteReminder(item.id)}
                aria-label="Delete reminder"
              >
                <Trash2 size={18} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
