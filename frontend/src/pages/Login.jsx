import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

function Login() {
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    setTimeout(() => {
      // ===============================
      // GET REGISTERED USER
      // ===============================
      const savedUser = localStorage.getItem("identityGuardUser");

      if (!savedUser) {
        setLoading(false);
        setError(
          "No account found. Please create an account first."
        );
        return;
      }

      // ===============================
      // READ USER DATA
      // ===============================
      let user;

      try {
        user = JSON.parse(savedUser);
      } catch {
        setLoading(false);
        setError(
          "Account data is corrupted. Please create your account again."
        );
        return;
      }

      // ===============================
      // EMAIL CHECK
      // ===============================
      if (
        user.email?.toLowerCase().trim() !==
        email.toLowerCase().trim()
      ) {
        setLoading(false);
        setError("Invalid email or password.");
        return;
      }

      // ===============================
      // PASSWORD CHECK
      // ===============================
      if (user.password !== password) {
        setLoading(false);
        setError("Invalid email or password.");
        return;
      }

      // ===============================
      // LOGIN SUCCESS
      // ===============================

      // Clear any old/stale session first
      localStorage.removeItem("identityGuardLoggedIn");

      // Main authentication flag
      localStorage.setItem("isLoggedIn", "true");

      // Current logged-in user
      localStorage.setItem(
        "currentUser",
        JSON.stringify({
          name: user.name,
          email: user.email,
        })
      );

      // Remember me
      if (rememberMe) {
        localStorage.setItem("rememberMe", "true");
      } else {
        localStorage.removeItem("rememberMe");
      }

      setLoading(false);

      // ===============================
      // REDIRECT
      // ===============================

      const redirectTo =
        location.state?.from || "/dashboard";

      navigate(redirectTo, {
        replace: true,
      });
    }, 700);
  };

  const handleForgotPassword = () => {
    alert("Password reset feature will be added soon.");
  };

  return (
    <div className="auth-page">

      {/* Background glow */}
      <div className="auth-glow auth-glow-one"></div>
      <div className="auth-glow auth-glow-two"></div>

      <div className="auth-container">

        {/* ================= LEFT SIDE ================= */}

        <section className="auth-intro">

          <div className="auth-brand-row">

            <Link to="/" className="auth-brand">

              <span>🛡️</span>

              <div>
                <strong>Identity Guard</strong>
                <small>AI FRAUD PROTECTION</small>
              </div>

            </Link>

            <Link
              to="/"
              className="auth-home-link"
            >
              ← Home
            </Link>

          </div>

          <div className="auth-hero">

            <div className="auth-status">

              <span></span>

              AI SECURITY SYSTEM

            </div>

            <h1>
              Protect every
              <span> transaction.</span>
            </h1>

            <p>
              Detect suspicious financial activity using
              machine learning and intelligent fraud analysis.
            </p>

          </div>

          <div className="auth-features">

            <div className="auth-feature">
              <span>✓</span>
              <p>Real-time fraud detection</p>
            </div>

            <div className="auth-feature">
              <span>✓</span>
              <p>Random Forest ML model</p>
            </div>

            <div className="auth-feature">
              <span>✓</span>
              <p>Secure transaction analysis</p>
            </div>

          </div>

        </section>


        {/* ================= LOGIN CARD ================= */}

        <section className="auth-card">

          <div className="auth-card-icon">
            🔐
          </div>

          <div className="auth-card-heading">

            <h2>Welcome back</h2>

            <p className="auth-card-subtitle">
              Sign in to your Identity Guard account
            </p>

          </div>


          {/* ERROR */}

          {error && (
            <div className="auth-error">
              ⚠️
              <span>{error}</span>
            </div>
          )}


          {/* LOGIN FORM */}

          <form onSubmit={handleSubmit}>

            {/* EMAIL */}

            <div className="auth-input-group">

              <label htmlFor="email">
                Email Address
              </label>

              <div className="auth-input-wrapper">

                <span>✉️</span>

                <input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    setError("");
                  }}
                  autoComplete="email"
                  required
                />

              </div>

            </div>


            {/* PASSWORD */}

            <div className="auth-input-group">

              <div className="auth-label-row">

                <label htmlFor="password">
                  Password
                </label>

                <button
                  type="button"
                  className="forgot-button"
                  onClick={handleForgotPassword}
                >
                  Forgot password?
                </button>

              </div>

              <div className="auth-input-wrapper">

                <span>🔒</span>

                <input
                  id="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    setError("");
                  }}
                  autoComplete="current-password"
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                >
                  {showPassword ? "🙈" : "👁️"}
                </button>

              </div>

            </div>


            {/* REMEMBER ME */}

            <label className="remember-row">

              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) =>
                  setRememberMe(e.target.checked)
                }
              />

              <span>Remember me</span>

            </label>


            {/* LOGIN BUTTON */}

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >

              {loading ? (
                <>
                  <span className="login-spinner"></span>
                  Signing in...
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <span>→</span>
                </>
              )}

            </button>

          </form>


          {/* DIVIDER */}

          <div className="auth-divider">
            <span>OR</span>
          </div>


          {/* SIGNUP */}

          <p className="auth-signup">

            Don't have an account?{" "}

            <Link to="/signup">
              Create account →
            </Link>

          </p>


          {/* SECURITY */}

          <div className="auth-security-note">

            <span>🛡️</span>

            <span>
              Your session is protected
            </span>

          </div>

        </section>

      </div>

    </div>
  );
}

export default Login;