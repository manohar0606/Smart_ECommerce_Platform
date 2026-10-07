import { useEffect, useState } from "react";
import {
  getNotifications,
  markNotificationRead,
} from "../services/api";

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Please login first.");
      window.location.href = "/login";
      return;
    }

    try {
      const response = await getNotifications(token);
      setNotifications(response.data);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to load notifications."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (notificationId) => {
    const token = localStorage.getItem("access_token");

    try {
      await markNotificationRead(notificationId, token);

      setNotifications((current) =>
        current.map((notification) =>
          notification.id === notificationId
            ? { ...notification, is_read: true }
            : notification
        )
      );
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Unable to mark notification as read."
      );
    }
  };

  const getIcon = (type) => {
    if (type === "order") return "📦";
    if (type === "payment") return "💳";
    return "🔔";
  };

  return (
    <div style={styles.page}>
      <div style={styles.logo}>OrderNow</div>

      <h1 style={styles.title}>
        My <span style={styles.accent}>Notifications</span>
      </h1>

      <p style={styles.subtitle}>
        Stay updated with your orders and account activity.
      </p>

      {loading && (
        <div style={styles.message}>
          Loading notifications...
        </div>
      )}

      {error && (
        <div style={styles.error}>
          {error}
        </div>
      )}

      {!loading && !error && notifications.length === 0 && (
        <div style={styles.message}>
          No notifications yet.
        </div>
      )}

      {!loading && !error && notifications.length > 0 && (
        <div>
          {notifications.map((notification) => (
            <div
              style={{
                ...styles.card,
                backgroundColor: notification.is_read
                  ? "#ffffff"
                  : "#eef8f7",
              }}
              key={notification.id}
            >
              <div style={styles.icon}>
                {getIcon(notification.type)}
              </div>

              <div style={styles.details}>
                <h3 style={styles.heading}>
                  {notification.type === "order"
                    ? "Order Update"
                    : "Notification"}
                </h3>

                <p style={styles.messageText}>
                  {notification.message}
                </p>

                <small style={styles.time}>
                  {new Date(
                    notification.timestamp
                  ).toLocaleString("en-IN")}
                </small>
              </div>

              {!notification.is_read && (
                <button
                  style={styles.readButton}
                  onClick={() =>
                    handleMarkAsRead(notification.id)
                  }
                >
                  Mark as Read
                </button>
              )}

              {notification.is_read && (
                <span style={styles.readBadge}>
                  Read
                </span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f4f8f8",
    padding: "40px 8%",
    fontFamily: '"Trebuchet MS", sans-serif',
  },

  logo: {
    fontSize: "30px",
    fontWeight: "800",
    color: "#0F766E",
    marginBottom: "35px",
  },

  title: {
    color: "#172121",
  },

  accent: {
    color: "#0F766E",
  },

  subtitle: {
    color: "#6b7280",
    marginBottom: "30px",
  },

  card: {
    border: "1px solid #dce7e6",
    borderRadius: "16px",
    padding: "20px",
    marginBottom: "15px",
    display: "flex",
    alignItems: "center",
    gap: "18px",
    boxShadow: "0 5px 18px rgba(15,118,110,0.05)",
  },

  icon: {
    width: "60px",
    height: "60px",
    borderRadius: "14px",
    background: "#e5f3f1",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "28px",
    flexShrink: 0,
  },

  details: {
    flex: 1,
  },

  heading: {
    marginBottom: "8px",
    color: "#172121",
  },

  messageText: {
    color: "#4b5f5e",
    marginBottom: "8px",
  },

  time: {
    color: "#888",
  },

  readButton: {
    border: "none",
    background: "#0F766E",
    color: "#ffffff",
    padding: "9px 14px",
    borderRadius: "9px",
    fontWeight: "700",
    cursor: "pointer",
  },

  readBadge: {
    background: "#dce7e6",
    color: "#55706e",
    padding: "7px 12px",
    borderRadius: "15px",
    fontSize: "12px",
    fontWeight: "700",
  },

  message: {
    background: "#ffffff",
    padding: "35px",
    borderRadius: "16px",
    textAlign: "center",
    color: "#666",
  },

  error: {
    background: "#fff0f0",
    color: "#c62828",
    padding: "20px",
    borderRadius: "12px",
  },
};

export default Notifications;