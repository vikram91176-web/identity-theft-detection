import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home-page">

      {/* NAVBAR */}
      <header className="home-navbar">
        <Link to="/" className="home-brand">
          <div className="brand-icon">🛡️</div>
          <div>
            <div className="brand-name">Identity Guard</div>
            <div className="brand-tagline">AI FRAUD PROTECTION</div>
          </div>
        </Link>

        <nav className="home-nav">
          <Link to="/">Home</Link>
          <Link to="/login">Login</Link>
          <Link to="/signup">Sign Up</Link>
        </nav>

        <Link to="/login" className="home-nav-button">
          Get Started <span>→</span>
        </Link>
      </header>


      {/* HERO */}
      <main>

        <section className="home-hero">

          <div className="hero-content">

            <div className="hero-badge">
              <span></span>
              AI-POWERED FINANCIAL SECURITY
            </div>

            <h1>
              Protect every
              <br />
              <span>transaction.</span>
            </h1>

            <p>
              Detect suspicious financial activity with machine learning
              and intelligent fraud analysis. Identity Guard helps keep
              your transactions safe in real time.
            </p>

            <div className="hero-actions">
              <Link to="/analyze" className="primary-button">
                Analyze Transaction
                <span>→</span>
              </Link>

              <Link to="/signup" className="secondary-button">
                Create Account
              </Link>
            </div>

            <div className="hero-trust">
              <span>✓ Real-time Detection</span>
              <span>✓ Random Forest ML</span>
              <span>✓ Secure Analysis</span>
            </div>

          </div>


          {/* HERO VISUAL */}
          <div className="hero-visual">

            <div className="security-orbit orbit-one"></div>
            <div className="security-orbit orbit-two"></div>

            <div className="security-card">

              <div className="security-card-top">
                <span className="live-dot"></span>
                SYSTEM ACTIVE
              </div>

              <div className="shield-large">
                🛡️
              </div>

              <h3>Transaction Protected</h3>

              <p>
                AI continuously monitors transaction patterns
                for suspicious activity.
              </p>

              <div className="security-progress">
                <span></span>
              </div>

              <div className="security-footer">
                <span>Fraud Detection</span>
                <strong>ACTIVE</strong>
              </div>

            </div>

          </div>

        </section>


        {/* FEATURES */}
        <section className="home-features">

          <div className="section-heading">
            <span>SMART PROTECTION</span>
            <h2>Intelligent fraud detection</h2>
            <p>
              Powerful machine learning tools designed to identify
              potentially fraudulent transactions.
            </p>
          </div>


          <div className="feature-grid">

            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3>Real-Time Detection</h3>
              <p>
                Analyze financial transactions instantly and
                identify suspicious activity.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>Machine Learning</h3>
              <p>
                Powered by a Random Forest model trained on
                transaction data for fraud classification.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🛡️</div>
              <h3>Secure Protection</h3>
              <p>
                Keep your financial transactions protected with
                intelligent risk analysis.
              </p>
            </div>

          </div>

        </section>


        {/* CTA */}
        <section className="home-cta">

          <div className="cta-icon">🛡️</div>

          <div>
            <span>SECURITY SYSTEM</span>
            <h2>Ready to protect your transactions?</h2>
            <p>
              Start analyzing suspicious financial activity
              with Identity Guard.
            </p>
          </div>

          <Link to="/analyze" className="primary-button">
            Get Started <span>→</span>
          </Link>

        </section>

      </main>


      {/* FOOTER */}
      <footer className="home-footer">
        <span>🛡️ Identity Guard</span>
        <span>AI-Powered Financial Security</span>
        <span>Random Forest ML</span>
      </footer>

    </div>
  );
}

export default Home;