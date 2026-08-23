import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Signup() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  // ==========================================
  // HANDLE INPUT
  // ==========================================

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    setError("");
    setSuccess("");
  };

  // ==========================================
  // CREATE ACCOUNT
  // ==========================================

  const handleSubmit = (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    const name = formData.name.trim();
    const email = formData.email.trim().toLowerCase();
    const password = formData.password;
    const confirmPassword = formData.confirmPassword;

    // ========================================
    // VALIDATION
    // ========================================

    if (
      !name ||
      !email ||
      !password ||
      !confirmPassword
    ) {
      setError("Please fill all fields.");
      return;
    }

    if (name.length < 2) {
      setError("Please enter a valid full name.");
      return;
    }

    if (password.length < 6) {
      setError(
        "Password must contain at least 6 characters."
      );
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    // ========================================
    // CHECK EXISTING ACCOUNT
    // ========================================

    const savedUser =
      localStorage.getItem("identityGuardUser");

    if (savedUser) {
      try {
        const existingUser = JSON.parse(savedUser);

        if (
          existingUser.email?.toLowerCase() ===
          email
        ) {
          setError(
            "An account with this email already exists. Please sign in."
          );
          return;
        }
      } catch (error) {
        // Invalid old data will be replaced below
        localStorage.removeItem(
          "identityGuardUser"
        );
      }
    }

    // ========================================
    // CREATE ACCOUNT
    // ========================================

    setLoading(true);

    setTimeout(() => {
      const newUser = {
        name,
        email,
        password,
      };

      // ======================================
      // SAVE USER
      // ======================================

      localStorage.setItem(
        "identityGuardUser",
        JSON.stringify(newUser)
      );

      // ======================================
      // VERY IMPORTANT:
      // NEW USER IS NOT LOGGED IN AUTOMATICALLY
      // ======================================

      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem(
        "identityGuardLoggedIn"
      );
      localStorage.removeItem("currentUser");
      localStorage.removeItem("rememberMe");

      // ======================================
      // SUCCESS
      // ======================================

      setLoading(false);

      setSuccess(
        "Account created successfully! Redirecting to login..."
      );

      // ======================================
      // GO TO LOGIN
      // ======================================

      setTimeout(() => {
        navigate("/login", {
          replace: true,
          state: {
            message:
              "Account created successfully. Please sign in.",
          },
        });
      }, 800);
    }, 700);
  };

  return (
    <div className="signup-page">

      {/* ======================================
          BACKGROUND GLOW
      ====================================== */}

      <div className="signup-glow signup-glow-one"></div>

      <div className="signup-glow signup-glow-two"></div>


      <div className="signup-wrapper">

        {/* ====================================
            LEFT SIDE
        ==================================== */}

        <section className="signup-hero">

          {/* BRAND */}

          <div className="signup-brand">

            <Link
              to="/"
              className="signup-brand-link"
            >

              <div className="brand-logo">
                🛡️
              </div>

              <div>

                <strong>
                  Identity Guard
                </strong>

                <span>
                  AI FRAUD PROTECTION
                </span>

              </div>

            </Link>


            {/* HOME BUTTON */}

            <Link
              to="/"
              className="signup-home-link"
            >
              ← Home
            </Link>

          </div>


          {/* BADGE */}

          <div className="signup-badge">

            <span></span>

            JOIN THE SECURITY SYSTEM

          </div>


          {/* HERO TITLE */}

          <h1>

            Protect every

            <br />

            <span>
              transaction.
            </span>

          </h1>


          <p className="signup-description">

            Create your secure account and start
            detecting suspicious financial activity
            using machine learning.

          </p>


          {/* FEATURES */}

          <div className="signup-features">

            <div className="signup-feature">

              <div>
                ✓
              </div>

              <span>
                Real-time fraud detection
              </span>

            </div>


            <div className="signup-feature">

              <div>
                ✓
              </div>

              <span>
                Random Forest ML model
              </span>

            </div>


            <div className="signup-feature">

              <div>
                ✓
              </div>

              <span>
                Secure transaction analysis
              </span>

            </div>

          </div>

        </section>


        {/* ====================================
            RIGHT SIDE
        ==================================== */}

        <section className="signup-form-area">

          <div className="signup-card">

            {/* ICON */}

            <div className="signup-card-icon">
              ✨
            </div>


            {/* HEADER */}

            <div className="signup-card-header">

              <h2>
                Create account
              </h2>

              <p>

                Start protecting your financial
                transactions with AI-powered detection.

              </p>

            </div>


            {/* ==================================
                ERROR
            ================================== */}

            {error && (

              <div className="signup-error">

                ⚠️

                <span>
                  {error}
                </span>

              </div>

            )}


            {/* ==================================
                SUCCESS
            ================================== */}

            {success && (

              <div className="signup-success">

                ✅

                <span>
                  {success}
                </span>

              </div>

            )}


            {/* ==================================
                FORM
            ================================== */}

            <form onSubmit={handleSubmit}>

              {/* NAME */}

              <div className="signup-field">

                <label htmlFor="name">
                  Full Name
                </label>

                <div className="signup-input-wrapper">

                  <span>
                    👤
                  </span>

                  <input
                    id="name"
                    type="text"
                    name="name"
                    placeholder="Enter your full name"
                    value={formData.name}
                    onChange={handleChange}
                    autoComplete="name"
                    disabled={loading}
                    required
                  />

                </div>

              </div>


              {/* EMAIL */}

              <div className="signup-field">

                <label htmlFor="signup-email">
                  Email Address
                </label>

                <div className="signup-input-wrapper">

                  <span>
                    ✉️
                  </span>

                  <input
                    id="signup-email"
                    type="email"
                    name="email"
                    placeholder="you@example.com"
                    value={formData.email}
                    onChange={handleChange}
                    autoComplete="email"
                    disabled={loading}
                    required
                  />

                </div>

              </div>


              {/* PASSWORD */}

              <div className="signup-field">

                <label htmlFor="signup-password">
                  Password
                </label>

                <div className="signup-input-wrapper">

                  <span>
                    🔒
                  </span>

                  <input
                    id="signup-password"
                    type="password"
                    name="password"
                    placeholder="Create a strong password"
                    value={formData.password}
                    onChange={handleChange}
                    autoComplete="new-password"
                    disabled={loading}
                    required
                  />

                </div>

              </div>


              {/* CONFIRM PASSWORD */}

              <div className="signup-field">

                <label htmlFor="confirm-password">
                  Confirm Password
                </label>

                <div className="signup-input-wrapper">

                  <span>
                    🔐
                  </span>

                  <input
                    id="confirm-password"
                    type="password"
                    name="confirmPassword"
                    placeholder="Confirm your password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    autoComplete="new-password"
                    disabled={loading}
                    required
                  />

                </div>

              </div>


              {/* ==================================
                  BUTTON
              ================================== */}

              <button
                type="submit"
                className="signup-submit"
                disabled={loading}
              >

                {loading ? (

                  <>
                    <span className="login-spinner"></span>

                    Creating account...
                  </>

                ) : (

                  <>
                    <span>
                      Create Secure Account
                    </span>

                    <strong>
                      →
                    </strong>
                  </>

                )}

              </button>

            </form>


            {/* ==================================
                SECURITY
            ================================== */}

            <div className="signup-security">

              <div className="security-box">

                <span>
                  🛡️
                </span>

                <div>

                  <strong>
                    Protected
                  </strong>

                  <small>
                    Your account is secure
                  </small>

                </div>

              </div>


              <div className="security-box">

                <span>
                  🤖
                </span>

                <div>

                  <strong>
                    AI Powered
                  </strong>

                  <small>
                    Smart fraud detection
                  </small>

                </div>

              </div>

            </div>


            {/* ==================================
                LOGIN
            ================================== */}

            <div className="signup-login">

              Already have an account?{" "}

              <Link to="/login">
                Sign in →
              </Link>

            </div>

          </div>

        </section>

      </div>

    </div>
  );
}

export default Signup;