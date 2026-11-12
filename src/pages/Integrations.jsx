
import React, { useEffect, useState, useCallback } from "react";
import { Link as LinkIcon, RefreshCw } from "lucide-react";

// Backend URL
const API_URL = "http://127.0.0.1:8000";

// Supported providers
const providers = ["GOOGLE_FIT", "APPLE_HEALTH"];

export default function Integrations() {
  const [integrations, setIntegrations] = useState([]);
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const token = localStorage.getItem("access_token");

  const getHeaders = () => ({
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  });

  // Handle API responses safely
  const handleResponse = async (response) => {
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      const detail = Array.isArray(data.detail)
        ? data.detail.map(item => item.msg).join(", ")
        : data.detail;

      throw new Error(detail || `Request failed: ${response.status}`);
    }

    return data;
  };

  // Load integrations
  const loadIntegrations = useCallback(async () => {
    try {
      setError("");

      const response = await fetch(
        `${API_URL}/phase3/integrations`,
        {
          method: "GET",
          headers: getHeaders()
        }
      );

      const data = await handleResponse(response);

      setIntegrations(Array.isArray(data) ? data : data.integrations || []);
    } catch (err) {
      setError(err.message);
    }
  }, [token]);

  useEffect(() => {
    loadIntegrations();
  }, [loadIntegrations]);

  // Connect provider
  async function connect(provider) {
  const integration = integrations.find(
    item => item.provider === provider
  );

  if (!integration) {
    setError("Integration record not found.");
    return;
  }

  const authorizationCode = window.prompt(
    "Enter OAuth authorization code:"
  );

  if (!authorizationCode) return;

  try {
    setLoading(true);
    setError("");

    const requestBody = {
      provider: provider,
      authorization_code: authorizationCode,
      redirect_uri: "http://localhost:5173/callback"
    };

    console.log("Connect request body:", requestBody);

    const response = await fetch(
      `${API_URL}/phase3/integrations/${integration.id}/connect`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify(requestBody)
      }
    );

    const data = await response.json();

    console.log("Connect API response:", data);

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail)
      );
    }

    setMessage("Integration connected successfully.");
    await loadIntegrations();

  } catch (err) {
    setError(err.message);
    console.error("Connect error:", err);
  } finally {
    setLoading(false);
  }
}
    
  // Disconnect provider
  async function disconnect(provider) {
    try {
      setLoading(true);
      setError("");
      setMessage("");

      const response = await fetch(
  `http://127.0.0.1:8000/phase3/integrations/${integration.id}/disconnect`,
  {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  }
);

      await handleResponse(response);

      setMessage(`${provider} disconnected successfully.`);
      await loadIntegrations();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // Synchronize activities
  async function sync() {
    try {
      setLoading(true);
      setError("");
      setMessage("");

      const response = await fetch(
        `${API_URL}/phase3/integrations/sync`,
        {
          method: "POST",
          headers: getHeaders(),
          // Confirm required fields in FitnessSyncRequest.
          body: JSON.stringify({})
        }
      );

      const data = await handleResponse(response);

      setActivities(data.activities || []);
      setMessage("Activity synchronization completed.");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="integrations-page">
      <div className="page-title">
        <h2>Fitness Integrations</h2>
        <p>Connect external health and fitness services.</p>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {message && (
        <div className="success-message">
          {message}
        </div>
      )}

      {providers.map(provider => {
        const integration = integrations.find(
          item => item.provider === provider
        );

        const connected = integration?.is_connected;

        return (
          <div className="panel integration-card" key={provider}>
            <div>
              <LinkIcon size={28} />

              <h3>
                {provider === "GOOGLE_FIT"
                  ? "Google Fit / Health Connect"
                  : "Apple Health"}
              </h3>

              <p>
                {connected ? "Connected" : "Not connected"}
              </p>
            </div>

            {connected ? (
              <button
                className="danger-button"
                onClick={() => disconnect(provider)}
                disabled={loading}
              >
                Disconnect
              </button>
            ) : (
              <button
                className="primary-button"
                onClick={() => connect(provider)}
                disabled={loading || !integration}
              >
                {integration ? "Connect" : "Setup Required"}
              </button>
            )}
          </div>
        );
      })}

      <div className="panel">
        <h3>Activity Synchronization</h3>

        <button
          className="primary-button"
          onClick={sync}
          disabled={loading}
        >
          <RefreshCw size={18} />
          {loading ? "Processing..." : "Sync Activities"}
        </button>

        {activities.map((activity, index) => (
          <div className="meal-row" key={activity.id || index}>
            <span>{activity.activity_type}</span>
            <strong>{activity.steps || 0} Steps</strong>
          </div>
        ))}
      </div>
    </div>
  );
}
