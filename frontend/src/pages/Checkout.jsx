import { useEffect, useState } from "react";
import {
  getCart,
  checkout,
  createPayment,
} from "../services/api";

function Checkout() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCart();
  }, []);

  const loadCart = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Please login first.");
      window.location.href = "/login";
      return;
    }

    try {
      const response = await getCart(token);
      setItems(response.data);
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Unable to load your cart."
      );
    } finally {
      setLoading(false);
    }
  };

  const total = items.reduce(
    (sum, item) =>
      sum +
      Number(item.product.price) * item.quantity,
    0
  );

  const handleCheckout = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Please login first.");
      window.location.href = "/login";
      return;
    }

    if (items.length === 0) {
      alert("Your cart is empty.");
      window.location.href = "/products";
      return;
    }

    try {
      const orderResponse = await checkout(token);

      const orderId = orderResponse.data.id;

      const paymentResponse = await createPayment(
        orderId,
        token
      );

      alert(
        `Payment successful!\n\nOrder ID: ${
          paymentResponse.data.order_id
        }\nAmount: ₹${Number(
          paymentResponse.data.amount
        ).toLocaleString("en-IN")}\nTransaction ID: ${
          paymentResponse.data.transaction_id
        }`
      );

      window.location.href = "/orders";
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Unable to complete your order."
      );
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.logo}>OrderNow</div>

      <h1 style={styles.title}>
        Secure <span style={styles.accent}>Checkout</span>
      </h1>

      <p style={styles.subtitle}>
        Enter your details and complete your order.
      </p>

      {loading ? (
        <div style={styles.message}>
          Loading your cart...
        </div>
      ) : (
        <div style={styles.content}>
          {/* Delivery Details */}
          <div style={styles.formCard}>
            <h2>Delivery Details</h2>

            <label style={styles.label}>Full Name</label>
            <input
              style={styles.input}
              type="text"
              placeholder="Enter your full name"
            />

            <label style={styles.label}>Email</label>
            <input
              style={styles.input}
              type="email"
              placeholder="Enter your email"
            />

            <label style={styles.label}>
              Phone Number
            </label>
            <input
              style={styles.input}
              type="tel"
              placeholder="Enter your phone number"
            />

            <label style={styles.label}>Address</label>
            <textarea
              style={styles.textarea}
              placeholder="Enter your delivery address"
              rows="4"
            />

            <button
              style={styles.button}
              onClick={handleCheckout}
            >
              Place Order & Pay →
            </button>
          </div>

          {/* Order Summary */}
          <div style={styles.summary}>
            <h2>Order Summary</h2>

            {items.length === 0 ? (
              <p style={styles.empty}>
                Your cart is empty.
              </p>
            ) : (
              <>
                {items.map((item) => (
                  <div
                    style={styles.row}
                    key={item.id}
                  >
                    <span>
                      {item.product.name} × {item.quantity}
                    </span>

                    <strong>
                      ₹
                      {(
                        Number(item.product.price) *
                        item.quantity
                      ).toLocaleString("en-IN")}
                    </strong>
                  </div>
                ))}

                <hr />

                <div style={styles.total}>
                  <span>Total</span>

                  <strong>
                    ₹{total.toLocaleString("en-IN")}
                  </strong>
                </div>
              </>
            )}
          </div>
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

  content: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "25px",
    alignItems: "start",
  },

  formCard: {
    background: "#ffffff",
    padding: "30px",
    borderRadius: "18px",
    border: "1px solid #dce7e6",
    boxShadow: "0 5px 18px rgba(15,118,110,0.05)",
  },

  summary: {
    background: "#ffffff",
    padding: "30px",
    borderRadius: "18px",
    border: "1px solid #dce7e6",
    boxShadow: "0 5px 18px rgba(15,118,110,0.05)",
    height: "fit-content",
  },

  label: {
    display: "block",
    marginTop: "18px",
    marginBottom: "8px",
    fontWeight: "600",
    color: "#263333",
  },

  input: {
    width: "100%",
    padding: "13px",
    border: "1px solid #d5dddd",
    borderRadius: "9px",
    fontSize: "15px",
    boxSizing: "border-box",
    outline: "none",
  },

  textarea: {
    width: "100%",
    padding: "13px",
    border: "1px solid #d5dddd",
    borderRadius: "9px",
    fontSize: "15px",
    boxSizing: "border-box",
    resize: "vertical",
    fontFamily: '"Trebuchet MS", sans-serif',
    outline: "none",
  },

  row: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "15px",
    margin: "18px 0",
  },

  total: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: "20px",
    fontSize: "20px",
  },

  button: {
    width: "100%",
    marginTop: "25px",
    padding: "14px",
    border: "none",
    borderRadius: "10px",
    background: "#0F766E",
    color: "#ffffff",
    fontWeight: "700",
    fontSize: "15px",
    cursor: "pointer",
  },

  message: {
    background: "#ffffff",
    padding: "35px",
    borderRadius: "16px",
    textAlign: "center",
    color: "#666",
  },

  empty: {
    color: "#777",
    textAlign: "center",
    padding: "20px 0",
  },
};

export default Checkout;