import { useState } from "react";
import { loginUser } from "../services/api";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await loginUser({
        email,
        password,
      });

      localStorage.setItem("access_token", response.data.access_token);

      alert("Login successful!");
      window.location.href = "/";
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Login failed. Please check your email and password."
      );
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <div style={styles.logo}>
          OrderNow
        </div>

        <h1 style={styles.title}>Welcome back</h1>

        <p style={styles.subtitle}>
          Login to continue shopping.
        </p>

        <form onSubmit={handleLogin}>
          <label style={styles.label}>Email</label>

          <input
            style={styles.input}
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label style={styles.label}>Password</label>

          <input
            style={styles.input}
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button style={styles.button} type="submit">
            Login →
          </button>
        </form>

        <p style={styles.bottomText}>
          Don't have an account?{" "}
          <a href="/register" style={styles.link}>
            Register
          </a>
        </p>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f4f8f8",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontFamily: '"Trebuchet MS", sans-serif',
    padding: "20px",
    boxSizing: "border-box",
  },

  card: {
    width: "400px",
    background: "#ffffff",
    padding: "40px",
    borderRadius: "20px",
    boxShadow: "0 12px 35px rgba(15, 118, 110, 0.12)",
    boxSizing: "border-box",
  },

  logo: {
    fontSize: "28px",
    fontWeight: "800",
    color: "#0F766E",
    marginBottom: "30px",
  },

  title: {
    fontSize: "32px",
    marginBottom: "8px",
    color: "#172121",
  },

  subtitle: {
    color: "#6b7280",
    marginBottom: "28px",
  },

  label: {
    display: "block",
    marginBottom: "7px",
    marginTop: "18px",
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

  button: {
    width: "100%",
    marginTop: "25px",
    padding: "14px",
    border: "none",
    borderRadius: "10px",
    background: "#0F766E",
    color: "#ffffff",
    fontSize: "16px",
    fontWeight: "700",
    cursor: "pointer",
  },

  bottomText: {
    textAlign: "center",
    color: "#777",
    marginTop: "22px",
  },

  link: {
    color: "#0F766E",
    fontWeight: "700",
    textDecoration: "none",
  },
};

export default Login;