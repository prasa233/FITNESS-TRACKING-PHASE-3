import { useState } from "react";
import api from "../services/api";
import { saveToken } from "../services/auth";

export default function Auth({ onAuthenticated }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const endpoint = mode === "login" ? "/auth/login" : "/auth/register";
      const { data } = await api.post(endpoint, { email, password });
      saveToken(data.access_token);
      onAuthenticated();
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
          "Could not connect to the server. Check that the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={styles.page}>
      <form onSubmit={handleSubmit} style={styles.card}>
        <div style={styles.brand}>FitTrack</div>
        <h1 style={styles.heading}>{mode === "login" ? "Welcome back" : "Create your account"}</h1>
        <p style={styles.subheading}>
          {mode === "login" ? "Sign in to continue to your fitness dashboard." : "Register to start tracking your fitness."}
        </p>

        <label style={styles.label} htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
          style={styles.input}
        />

        <label style={styles.label} htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          autoComplete={mode === "login" ? "current-password" : "new-password"}
          minLength={mode === "login" ? 1 : 8}
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
          style={styles.input}
        />

        {error && <p role="alert" style={styles.error}>{error}</p>}

        <button type="submit" disabled={loading} style={styles.button}>
          {loading ? "Please wait…" : mode === "login" ? "Sign in" : "Register"}
        </button>

        <p style={styles.switchText}>
          {mode === "login" ? "Don't have an account? " : "Already registered? "}
          <button
            type="button"
            onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(""); }}
            style={styles.switchButton}
          >
            {mode === "login" ? "Register" : "Sign in"}
          </button>
        </p>
      </form>
    </main>
  );
}

const styles = {
  page: { minHeight: "100vh", display: "grid", placeItems: "center", padding: 24, background: "#f3f6f4" },
  card: { width: "100%", maxWidth: 420, display: "flex", flexDirection: "column", padding: 36, borderRadius: 20, background: "white", boxShadow: "0 16px 45px rgba(20, 45, 30, .10)" },
  brand: { color: "#16834a", fontSize: 18, fontWeight: 800, letterSpacing: ".04em" },
  heading: { margin: "24px 0 8px", color: "#14251b", fontSize: 28 },
  subheading: { margin: "0 0 24px", color: "#66736a", lineHeight: 1.5 },
  label: { margin: "0 0 7px", color: "#29372f", fontWeight: 600 },
  input: { boxSizing: "border-box", width: "100%", marginBottom: 18, padding: "12px 14px", border: "1px solid #d7e0d9", borderRadius: 9, fontSize: 16 },
  error: { margin: "0 0 16px", color: "#b42318", fontSize: 14 },
  button: { padding: 13, border: 0, borderRadius: 9, background: "#16834a", color: "white", fontSize: 16, fontWeight: 700, cursor: "pointer" },
  switchText: { margin: "20px 0 0", textAlign: "center", color: "#66736a" },
  switchButton: { padding: 0, border: 0, background: "none", color: "#16834a", font: "inherit", fontWeight: 700, cursor: "pointer" },
};
