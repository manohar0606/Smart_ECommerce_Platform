import { useEffect, useState } from "react";
import { getCart, removeFromCart } from "../services/api";

function Cart() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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
      setError(
        error.response?.data?.detail ||
          "Unable to load your cart."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (productId) => {
    const token = localStorage.getItem("access_token");

    try {
      await removeFromCart(productId, token);

      setItems((currentItems) =>
        currentItems.filter(
          (item) => item.product_id !== productId
        )
      );

      alert("Product removed from cart.");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Unable to remove product."
      );
    }
  };

  const total = items.reduce(
    (sum, item) =>
      sum + Number(item.product.price) * item.quantity,
    0
  );

  return (
    <div style={styles.page}>
      <div style={styles.logo}>OrderNow</div>

      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>
            Your <span style={styles.accent}>Cart</span>
          </h1>

          <p style={styles.headerText}>
            Review your items before checkout.
          </p>
        </div>

        <a href="/products" style={styles.continue}>
          ← Continue Shopping
        </a>
      </div>

      {loading && (
        <div style={styles.message}>
          Loading your cart...
        </div>
      )}

      {error && (
        <div style={styles.error}>
          {error}
        </div>
      )}

      {!loading && !error && items.length === 0 && (
        <div style={styles.message}>
          Your cart is empty.
        </div>
      )}

      {!loading && !error && items.length > 0 && (
        <div style={styles.content}>
          <div>
            {items.map((item) => (
              <div style={styles.item} key={item.id}>
                <div style={styles.icon}>
                  {item.product.image_url &&
                  !item.product.image_url.includes("example.com") ? (
                    <img
                      src={item.product.image_url}
                      alt={item.product.name}
                      style={styles.image}
                    />
                  ) : (
                    <span>🛍️</span>
                  )}
                </div>

                <div style={styles.details}>
                  <h3>{item.product.name}</h3>

                  <p style={styles.description}>
                    {item.product.description}
                  </p>

                  <p>
                    Quantity: <strong>{item.quantity}</strong>
                  </p>

                  <strong style={styles.price}>
                    ₹
                    {Number(item.product.price).toLocaleString(
                      "en-IN"
                    )}
                  </strong>
                </div>

                <button
                  style={styles.removeButton}
                  onClick={() =>
                    handleRemove(item.product_id)
                  }
                >
                  Remove
                </button>
              </div>
            ))}
          </div>

          <div style={styles.summary}>
            <h2>Order Summary</h2>

            <div style={styles.row}>
              <span>Items</span>
              <strong>{items.length}</strong>
            </div>

            <div style={styles.row}>
              <span>Subtotal</span>
              <strong>
                ₹{total.toLocaleString("en-IN")}
              </strong>
            </div>

            <hr />

            <div style={styles.total}>
              <span>Total</span>
              <strong>
                ₹{total.toLocaleString("en-IN")}
              </strong>
            </div>

            <a
              href="/checkout"
              style={styles.button}
            >
              Proceed to Checkout →
            </a>
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

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "30px",
    gap: "20px",
  },

  title: {
    marginBottom: "8px",
  },

  accent: {
    color: "#0F766E",
  },

  headerText: {
    color: "#6b7280",
  },

  continue: {
    textDecoration: "none",
    color: "#0F766E",
    fontWeight: "600",
  },

  content: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "25px",
  },

  item: {
    background: "#ffffff",
    padding: "20px",
    borderRadius: "16px",
    display: "flex",
    alignItems: "center",
    marginBottom: "15px",
    border: "1px solid #dce7e6",
    boxShadow: "0 5px 18px rgba(15,118,110,0.05)",
    gap: "20px",
  },

  icon: {
    width: "100px",
    height: "100px",
    borderRadius: "14px",
    background: "#e5f3f1",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "42px",
    overflow: "hidden",
    flexShrink: 0,
  },

  image: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
  },

  details: {
    flex: 1,
  },

  description: {
    color: "#6b7280",
  },

  price: {
    fontSize: "18px",
    color: "#172121",
  },

  removeButton: {
    border: "1px solid #e05252",
    background: "#fff5f5",
    color: "#c62828",
    padding: "10px 15px",
    borderRadius: "9px",
    fontWeight: "700",
    cursor: "pointer",
  },

  summary: {
    background: "#ffffff",
    padding: "25px",
    borderRadius: "16px",
    border: "1px solid #dce7e6",
    height: "fit-content",
    boxShadow: "0 5px 18px rgba(15,118,110,0.05)",
  },

  row: {
    display: "flex",
    justifyContent: "space-between",
    margin: "20px 0",
  },

  total: {
    display: "flex",
    justifyContent: "space-between",
    margin: "20px 0",
    fontSize: "20px",
  },

  button: {
    display: "block",
    width: "100%",
    boxSizing: "border-box",
    padding: "14px",
    borderRadius: "10px",
    background: "#0F766E",
    color: "#ffffff",
    textDecoration: "none",
    textAlign: "center",
    fontWeight: "700",
    marginTop: "20px",
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

export default Cart;