import { useEffect, useState } from "react";
import { getOrders } from "../services/api";

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Please login first.");
      window.location.href = "/login";
      return;
    }

    try {
      const response = await getOrders(token);
      setOrders(response.data);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Unable to load your orders."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.logo}>OrderNow</div>

      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>
            My <span style={styles.accent}>Orders</span>
          </h1>

          <p style={styles.subtitle}>
            Track your recent orders and delivery status.
          </p>
        </div>

        <a href="/products" style={styles.shopButton}>
          Continue Shopping →
        </a>
      </div>

      {loading && (
        <div style={styles.message}>
          Loading your orders...
        </div>
      )}

      {error && (
        <div style={styles.error}>
          {error}
        </div>
      )}

      {!loading && !error && orders.length === 0 && (
        <div style={styles.message}>
          You have no orders yet.
        </div>
      )}

      {!loading && !error && orders.length > 0 && (
        <div>
          {orders.map((order) => {
            const firstItem = order.items?.[0];

            return (
              <div style={styles.card} key={order.id}>
                <div style={styles.icon}>📦</div>

                <div style={styles.details}>
                  <h2 style={styles.orderId}>
                    Order #{order.id}
                  </h2>

                  <p style={styles.date}>
                    Order Date:{" "}
                    {new Date(order.timestamp).toLocaleDateString(
                      "en-IN"
                    )}
                  </p>

                  {firstItem && (
                    <p style={styles.product}>
                      {firstItem.product.name} × {firstItem.quantity}
                    </p>
                  )}

                  <strong style={styles.total}>
                    ₹{Number(order.total).toLocaleString("en-IN")}
                  </strong>
                </div>

                <div style={styles.statusSection}>
                  <div style={styles.status}>
                    {order.order_status}
                  </div>

                  <small style={styles.payment}>
                    Payment: {order.payment_status}
                  </small>
                </div>
              </div>
            );
          })}
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

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "30px",
    gap: "20px",
  },

  title: {
    marginBottom: "8px",
    color: "#172121",
  },

  accent: {
    color: "#0F766E",
  },

  subtitle: {
    color: "#6b7280",
    margin: 0,
  },

  shopButton: {
    textDecoration: "none",
    background: "#0F766E",
    color: "#ffffff",
    padding: "12px 20px",
    borderRadius: "10px",
    fontWeight: "600",
  },

  card: {
    background: "#ffffff",
    border: "1px solid #dce7e6",
    borderRadius: "18px",
    padding: "22px",
    marginBottom: "16px",
    display: "flex",
    alignItems: "center",
    gap: "20px",
    boxShadow: "0 5px 18px rgba(15,118,110,0.05)",
  },

  icon: {
    width: "70px",
    height: "70px",
    borderRadius: "14px",
    background: "#e5f3f1",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "32px",
    flexShrink: 0,
  },

  details: {
    flex: 1,
  },

  orderId: {
    marginBottom: "10px",
    fontSize: "20px",
    color: "#172121",
  },

  date: {
    color: "#777",
    marginBottom: "8px",
  },

  product: {
    marginBottom: "8px",
  },

  total: {
    fontSize: "18px",
    color: "#172121",
  },

  statusSection: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-end",
    gap: "10px",
  },

  status: {
    padding: "9px 15px",
    borderRadius: "20px",
    background: "#e5f3f1",
    color: "#0F766E",
    fontWeight: "700",
    fontSize: "14px",
    textTransform: "capitalize",
  },

  payment: {
    color: "#777",
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

export default Orders;