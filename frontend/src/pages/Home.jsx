function Home() {
  return (
    <div style={styles.page}>
      {/* Navbar */}
      <nav style={styles.navbar}>
        <div style={styles.logo}>OrderNow</div>

        <div style={styles.navLinks}>
          <a href="/" style={styles.navLink}>
            Home
          </a>

          <a href="/products" style={styles.navLink}>
            Products
          </a>

          <a href="/orders" style={styles.navLink}>
            Orders
          </a>

          <a href="/notifications" style={styles.navLink}>
            Notifications
          </a>

          <a href="/login" style={styles.navLink}>
            Login
          </a>

          <a href="/cart" style={styles.cartButton}>
            🛒 Cart
          </a>
        </div>
      </nav>

      {/* Hero */}
      <section style={styles.hero}>
        <div style={styles.heroText}>
          <p style={styles.smallTitle}>
            EASY SHOPPING. FAST DELIVERY.
          </p>

          <h1 style={styles.heroTitle}>
            Everything you need,
            <br />
            <span style={styles.highlight}>
              delivered to your door.
            </span>
          </h1>

          <p style={styles.heroDescription}>
            Discover quality products, great prices and a simple
            shopping experience designed for everyone.
          </p>

          <div style={styles.heroButtons}>
            <a href="/products" style={styles.shopButton}>
              Shop Now →
            </a>

            <a href="/products" style={styles.exploreButton}>
              Explore Products
            </a>
          </div>
        </div>

        <div style={styles.heroCard}>
          <div style={styles.heroIcon}>🛍️</div>

          <h2 style={styles.heroCardTitle}>
            Great Deals
          </h2>

          <p style={styles.heroCardText}>
            Find your favourites at the right price.
          </p>
        </div>
      </section>

      {/* Categories */}
      <section style={styles.section}>
        <div style={styles.sectionHeader}>
          <div>
            <p style={styles.sectionSmallTitle}>
              EXPLORE
            </p>

            <h2 style={styles.sectionTitle}>
              Shop by Category
            </h2>
          </div>

          <a href="/products" style={styles.viewButton}>
            View Products →
          </a>
        </div>

        <div style={styles.categoryGrid}>
          <div style={styles.categoryCard}>
            <div style={styles.categoryIcon}>💻</div>
            <h3>Electronics</h3>
            <p>Latest gadgets and devices</p>
          </div>

          <div style={styles.categoryCard}>
            <div style={styles.categoryIcon}>👕</div>
            <h3>Fashion</h3>
            <p>Trendy styles for everyone</p>
          </div>

          <div style={styles.categoryCard}>
            <div style={styles.categoryIcon}>🏠</div>
            <h3>Home</h3>
            <p>Everything for your home</p>
          </div>

          <div style={styles.categoryCard}>
            <div style={styles.categoryIcon}>🎧</div>
            <h3>Accessories</h3>
            <p>Useful products for everyday life</p>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section style={styles.section}>
        <div style={styles.sectionHeader}>
          <div>
            <p style={styles.sectionSmallTitle}>
              TRENDING NOW
            </p>

            <h2 style={styles.sectionTitle}>
              Featured Products
            </h2>
          </div>

          <a href="/products" style={styles.viewButton}>
            View All →
          </a>
        </div>

        <div style={styles.productGrid}>
          <div style={styles.productCard}>
            <div style={styles.productImage}>📱</div>
            <h3>Smartphone</h3>
            <p>Modern performance and design</p>
            <strong>₹24,999</strong>
          </div>

          <div style={styles.productCard}>
            <div style={styles.productImage}>🎧</div>
            <h3>Wireless Headphones</h3>
            <p>Clear sound and comfortable fit</p>
            <strong>₹2,999</strong>
          </div>

          <div style={styles.productCard}>
            <div style={styles.productImage}>⌚</div>
            <h3>Smart Watch</h3>
            <p>Track your day smarter</p>
            <strong>₹4,999</strong>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section style={styles.cta}>
        <div>
          <p style={styles.ctaSmall}>
            READY TO SHOP?
          </p>

          <h2 style={styles.ctaTitle}>
            Find something you'll love.
          </h2>

          <p style={styles.ctaText}>
            Browse our collection and start shopping today.
          </p>
        </div>

        <a href="/products" style={styles.ctaButton}>
          Start Shopping →
        </a>
      </section>

      {/* Footer */}
      <footer style={styles.footer}>
        <div>
          <div style={styles.footerLogo}>
            OrderNow
          </div>

          <p style={styles.footerText}>
            Simple shopping. Fast ordering.
          </p>
        </div>

        <p style={styles.footerCopyright}>
          © 2026 OrderNow
        </p>
      </footer>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f4f8f8",
    color: "#172121",
    fontFamily: '"Trebuchet MS", sans-serif',
  },

  navbar: {
    minHeight: "72px",
    padding: "0 8%",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    background: "#ffffff",
    borderBottom: "1px solid #dce7e6",
    gap: "20px",
  },

  logo: {
    fontSize: "28px",
    fontWeight: "800",
    color: "#0F766E",
    whiteSpace: "nowrap",
  },

  navLinks: {
    display: "flex",
    alignItems: "center",
    gap: "20px",
    flexWrap: "wrap",
    justifyContent: "flex-end",
  },

  navLink: {
    textDecoration: "none",
    color: "#334444",
    fontSize: "15px",
    fontWeight: "600",
  },

  cartButton: {
    textDecoration: "none",
    background: "#0F766E",
    color: "#ffffff",
    padding: "11px 18px",
    borderRadius: "10px",
    fontWeight: "700",
    whiteSpace: "nowrap",
  },

  hero: {
    margin: "35px auto",
    width: "84%",
    minHeight: "430px",
    borderRadius: "25px",
    padding: "55px",
    boxSizing: "border-box",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "40px",
    background: "linear-gradient(135deg, #103c3a, #0F766E)",
    color: "#ffffff",
  },

  heroText: {
    maxWidth: "650px",
  },

  smallTitle: {
    fontSize: "13px",
    letterSpacing: "2px",
    color: "#cce8e5",
    fontWeight: "700",
  },

  heroTitle: {
    fontSize: "52px",
    lineHeight: "1.1",
    margin: "15px 0",
  },

  highlight: {
    color: "#ffd166",
  },

  heroDescription: {
    fontSize: "17px",
    color: "#e4f4f2",
    lineHeight: "1.6",
    maxWidth: "580px",
  },

  heroButtons: {
    display: "flex",
    gap: "15px",
    marginTop: "30px",
    flexWrap: "wrap",
  },

  shopButton: {
    padding: "14px 25px",
    borderRadius: "10px",
    background: "#ffffff",
    color: "#0F766E",
    fontWeight: "700",
    textDecoration: "none",
  },

  exploreButton: {
    padding: "14px 25px",
    borderRadius: "10px",
    border: "1px solid #b8d8d5",
    background: "transparent",
    color: "#ffffff",
    textDecoration: "none",
  },

  heroCard: {
    width: "260px",
    height: "260px",
    borderRadius: "25px",
    background: "rgba(255,255,255,0.12)",
    border: "1px solid rgba(255,255,255,0.22)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    flexShrink: 0,
  },

  heroIcon: {
    fontSize: "70px",
    marginBottom: "10px",
  },

  heroCardTitle: {
    marginBottom: "8px",
  },

  heroCardText: {
    color: "#e4f4f2",
  },

  section: {
    width: "84%",
    margin: "70px auto",
  },

  sectionHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "20px",
    marginBottom: "28px",
  },

  sectionSmallTitle: {
    fontSize: "12px",
    letterSpacing: "2px",
    color: "#0F766E",
    fontWeight: "700",
    marginBottom: "6px",
  },

  sectionTitle: {
    fontSize: "30px",
    margin: "0",
  },

  viewButton: {
    color: "#0F766E",
    textDecoration: "none",
    fontWeight: "700",
  },

  categoryGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "18px",
  },

  categoryCard: {
    background: "#ffffff",
    borderRadius: "18px",
    padding: "25px",
    border: "1px solid #dce7e6",
  },

  categoryIcon: {
    fontSize: "38px",
    marginBottom: "15px",
  },

  productGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: "20px",
  },

  productCard: {
    background: "#ffffff",
    borderRadius: "18px",
    padding: "20px",
    border: "1px solid #dce7e6",
  },

  productImage: {
    height: "210px",
    borderRadius: "15px",
    background: "#e5f3f1",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "70px",
    marginBottom: "20px",
  },

  cta: {
    width: "84%",
    margin: "70px auto",
    padding: "40px",
    boxSizing: "border-box",
    borderRadius: "20px",
    background: "#dff1ef",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: "25px",
  },

  ctaSmall: {
    color: "#0F766E",
    fontSize: "12px",
    fontWeight: "700",
    letterSpacing: "2px",
  },

  ctaTitle: {
    marginBottom: "8px",
  },

  ctaText: {
    color: "#58706f",
  },

  ctaButton: {
    background: "#0F766E",
    color: "#ffffff",
    textDecoration: "none",
    padding: "15px 25px",
    borderRadius: "10px",
    fontWeight: "700",
    whiteSpace: "nowrap",
  },

  footer: {
    padding: "35px 8%",
    background: "#103c3a",
    color: "#ffffff",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "20px",
  },

  footerLogo: {
    fontSize: "25px",
    fontWeight: "800",
  },

  footerText: {
    color: "#cce8e5",
    marginTop: "8px",
  },

  footerCopyright: {
    color: "#cce8e5",
  },
};

export default Home;