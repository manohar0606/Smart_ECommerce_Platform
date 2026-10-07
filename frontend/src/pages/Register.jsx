import { useState } from "react";
import { registerUser } from "../services/api";

function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      await registerUser({
        name,
        email,
        password,
        phone,
      });

      alert("Registration successful!");
      window.location.href = "/login";
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Registration failed. Please try again."
      );
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <div style={styles.logo}>OrderNow</div>

        <h1 style={styles.title}>Create account</h1>

        <p style={styles.subtitle}>
          Join OrderNow and start shopping smarter.
        </p>

        <form onSubmit={handleRegister}>
          <label style={styles.label}>Full Name</label>

          <input
            style={styles.input}
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

          <label style={styles.label}>Email</label>

          <input
            style={styles.input}
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label style={styles.label}>Phone Number</label>

          <input
            style={styles.input}
            type="tel"
            placeholder="Enter your phone number"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
          />

          <label style={styles.label}>Password</label>

          <input
            style={styles.input}
            type="password"
            placeholder="Create a password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button style={styles.button} type="submit">
            Create Account →
          </button>
        </form>

        <p style={styles.bottomText}>
          Already have an account?{" "}
          <a href="/login" style={styles.link}>
            Login
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

export default Register;