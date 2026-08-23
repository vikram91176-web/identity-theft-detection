import { Link, useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  // ==========================================
  // LOGOUT
  // ==========================================
  const handleLogout = () => {
    // Remove current login session
    localStorage.removeItem("isLoggedIn");

    // Remove current logged-in user
    localStorage.removeItem("currentUser");

    // Remove remember-me session
    localStorage.removeItem("rememberMe");

    // Remove old authentication key
    localStorage.removeItem("identityGuardLoggedIn");

    // Go to login page
    navigate("/login", {
      replace: true,
    });
  };

  // ==========================================
  // GET CURRENT USER
  // ==========================================
  const currentUser = JSON.parse(
    localStorage.getItem("currentUser") || "null"
  );

  const userName = currentUser?.name || "User";

  return (
    <div className="dashboard-page">

      {/* ================= HEADER ================= */}
      <header className="dashboard-header">

        <Link
          to="/dashboard"
          className="dashboard-brand"
        >
          <span className="dashboard-brand-icon">
            🛡️
          </span>

          <div>
            <strong>Identity Guard</strong>
            <small>AI FRAUD PROTECTION</small>
          </div>
        </Link>


        {/* NAVIGATION */}
        <nav className="dashboard-nav">

          <Link
            to="/dashboard"
            className="active"
          >
            Dashboard
          </Link>

          <Link to="/analyze">
            Analyze
          </Link>

          <Link to="/history">
            History
          </Link>

        </nav>


        {/* LOGOUT */}
        <button
          type="button"
          className="logout-button"
          onClick={handleLogout}
        >
          Logout
        </button>

      </header>


      {/* ================= MAIN ================= */}
      <main className="dashboard-main">

        {/* ================= HERO ================= */}
        <section className="dashboard-hero">

          <div className="dashboard-hero-content">

            <span className="dashboard-status">

              <span></span>

              SYSTEM PROTECTED

            </span>


            <h1>
              Welcome back,{" "}
              <span>{userName}</span> 👋
            </h1>


            <p>
              Monitor and protect your financial
              transactions with AI-powered fraud detection.
            </p>

          </div>


          <div className="dashboard-hero-icon">
            🛡️
          </div>

        </section>


        {/* ================= STATUS CARDS ================= */}

        <section className="dashboard-status-grid">

          <div className="status-card">

            <div className="status-icon purple">
              🔍
            </div>

            <div>
              <small>Detection</small>
              <strong>Real-time</strong>
            </div>

          </div>


          <div className="status-card">

            <div className="status-icon green">
              🛡️
            </div>

            <div>
              <small>Protection</small>
              <strong>Active</strong>
            </div>

          </div>


          <div className="status-card">

            <div className="status-icon blue">
              🤖
            </div>

            <div>
              <small>AI Model</small>
              <strong>Random Forest</strong>
            </div>

          </div>


          <div className="status-card">

            <div className="status-icon orange">
              ⚡
            </div>

            <div>
              <small>Response</small>
              <strong>Fast</strong>
            </div>

          </div>

        </section>


        {/* ================= ACTION CARDS ================= */}

        <section className="dashboard-actions">

          {/* ANALYZE */}

          <div className="dashboard-action-card">

            <div className="action-card-top">

              <div className="action-icon">
                🔍
              </div>

              <span className="action-badge purple-badge">
                AI POWERED
              </span>

            </div>


            <h2>
              Analyze Transaction
            </h2>


            <p>
              Analyze any financial transaction and
              detect potentially fraudulent activity
              using our trained machine learning model.
            </p>


            <Link
              to="/analyze"
              className="dashboard-action-button"
            >
              Start Analysis
              <span>→</span>
            </Link>

          </div>


          {/* HISTORY */}

          <div className="dashboard-action-card">

            <div className="action-card-top">

              <div className="action-icon blue-icon">
                📊
              </div>

              <span className="action-badge blue-badge">
                INSIGHTS
              </span>

            </div>


            <h2>
              Transaction History
            </h2>


            <p>
              Review your previous transaction analyses,
              fraud probabilities and risk levels in one place.
            </p>


            <Link
              to="/history"
              className="dashboard-action-button"
            >
              View History
              <span>→</span>
            </Link>

          </div>


          {/* MODEL */}

          <div className="dashboard-action-card">

            <div className="action-card-top">

              <div className="action-icon green-icon">
                🤖
              </div>

              <span className="action-badge green-badge">
                ACTIVE
              </span>

            </div>


            <h2>
              AI Detection Model
            </h2>


            <p>
              Random Forest machine learning model trained
              on PaySim transaction data for fraud classification.
            </p>


            <div className="model-running">

              <span></span>

              Model is running

            </div>

          </div>

        </section>


        {/* ================= SECURITY STATUS ================= */}

        <section className="security-status">

          <div className="security-icon">
            🛡️
          </div>


          <div className="security-content">

            <span>
              SECURITY STATUS
            </span>


            <h2>
              Your transactions are protected
            </h2>


            <p>
              Identity Guard continuously analyzes
              transaction patterns to identify
              suspicious financial activity.
            </p>

          </div>


          <div className="protected-badge">

            <span></span>

            Protected

          </div>

        </section>

      </main>


      {/* ================= FOOTER ================= */}

      <footer className="dashboard-footer">

        <span>
          🛡️ Identity Guard
        </span>

        <span>
          AI-Powered Financial Security
        </span>

        <span>
          Random Forest ML
        </span>

      </footer>

    </div>
  );
}

export default Dashboard;