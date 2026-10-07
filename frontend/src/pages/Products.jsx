import { useEffect, useState } from "react";
import { getProducts, addToCart } from "../services/api";

function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const response = await getProducts();
      setProducts(response.data);
    } catch (error) {
      setError("Unable to load products.");
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async (productId) => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Please login first.");
      window.location.href = "/login";
      return;
    }

    try {
      await addToCart(
        {
          product_id: productId,
          quantity: 1,
        },
        token
      );

      alert("Product added to cart!");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Unable to add product to cart."
      );
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <div>
          <div style={styles.logo}>OrderNow</div>

          <p style={styles.subtitle}>
            Explore our latest products
          </p>
        </div>

        <a href="/cart" style={styles.cartButton}>
          🛒 Cart
        </a>
      </div>

      {loading && (
        <div style={styles.message}>
          Loading products...
        </div>
      )}

      {error && (
        <div style={styles.error}>
          {error}
        </div>
      )}

      {!loading && !error && products.length === 0 && (
        <div style={styles.message}>
          No products available.
        </div>
      )}

      <div style={styles.grid}>
        {products.map((product) => (
          <div style={styles.card} key={product.id}>
            <div style={styles.image}>
              {product.image_url &&
              !product.image_url.includes("example.com") ? (
                <img
                  src={product.image_url}
                  alt={product.name}
                  style={styles.productImage}
                />
              ) : (
                <span style={styles.emoji}>🛍️</span>
              )}
            </div>

            <div style={styles.category}>
              {product.category}
            </div>

            <h2 style={styles.name}>{product.name}</h2>

            <p style={styles.description}>
              {product.description}
            </p>

            <div style={styles.bottom}>
              <strong style={styles.price}>
                ₹{Number(product.price).toLocaleString("en-IN")}
              </strong>

              <span style={styles.stock}>
                {product.stock > 0
                  ? `${product.stock} in stock`
                  : "Out of stock"}
              </span>
            </div>

            <button
              onClick={() => handleAddToCart(product.id)}
              style={styles.button}
              disabled={product.stock <= 0}
            >
              Add to Cart
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f4f8f8",
    padding: "40px 7%",
    fontFamily: '"Trebuchet MS", sans-serif',
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "35px",
  },

  logo: {
    fontSize: "30px",
    fontWeight: "800",
    color: "#0F766E",
    marginBottom: "8px",
  },

  subtitle: {
    color: "#6b7280",
    margin: 0,
    fontSize: "16px",
  },

  cartButton: {
    textDecoration: "none",
    background: "#0F766E",
    color: "#fff",
    padding: "12px 20px",
    borderRadius: "10px",
    fontWeight: "600",
  },

  message: {
    background: "#fff",
    padding: "30px",
    borderRadius: "15px",
    textAlign: "center",
    color: "#666",
  },

  error: {
    background: "#fff0f0",
    color: "#c62828",
    padding: "20px",
    borderRadius: "12px",
    marginBottom: "20px",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "22px",
  },

  card: {
    background: "#fff",
    borderRadius: "18px",
    padding: "18px",
    border: "1px solid #dce7e6",
    boxShadow: "0 5px 18px rgba(15,118,110,0.07)",
  },

  image: {
    height: "190px",
    borderRadius: "14px",
    background: "#e5f3f1",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    overflow: "hidden",
    marginBottom: "18px",
  },

  productImage: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
  },

  emoji: {
    fontSize: "65px",
  },

  category: {
    color: "#0F766E",
    fontSize: "13px",
    fontWeight: "700",
    marginBottom: "8px",
    textTransform: "uppercase",
  },

  name: {
    fontSize: "20px",
    marginBottom: "8px",
    color: "#172121",
  },

  description: {
    color: "#6b7280",
    lineHeight: "1.5",
    minHeight: "45px",
  },

  bottom: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: "15px",
    gap: "10px",
  },

  price: {
    fontSize: "19px",
    color: "#172121",
  },

  stock: {
    fontSize: "12px",
    color: "#666",
  },

  button: {
    width: "100%",
    border: "none",
    background: "#0F766E",
    color: "#fff",
    padding: "12px",
    borderRadius: "9px",
    marginTop: "18px",
    fontWeight: "600",
    cursor: "pointer",
  },
};

export default Products;