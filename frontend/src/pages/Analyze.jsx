import { useState } from "react";
import { Link } from "react-router-dom";

const API_URL = "http://127.0.0.1:8000";

function Analyze() {

  // Authentication is handled by ProtectedRoute in App.jsx.
  // Do NOT redirect or return null here because that can break React Hooks.

  // =========================
  // FORM DATA
  // =========================
  const [formData, setFormData] = useState({
    step: 1,
    type: "TRANSFER",
    amount: 181,
    oldbalanceOrg: 181,
    newbalanceOrig: 0,
    oldbalanceDest: 0,
    newbalanceDest: 0,
    isFlaggedFraud: 0,
  });

  // =========================
  // RESULT
  // =========================
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // =========================
  // HANDLE INPUT
  // =========================
  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "type"
          ? value
          : Number(value),
    }));
  };

  // =========================
  // RESET
  // =========================
  const handleReset = () => {
    setFormData({
      step: 1,
      type: "TRANSFER",
      amount: 181,
      oldbalanceOrg: 181,
      newbalanceOrig: 0,
      oldbalanceDest: 0,
      newbalanceDest: 0,
      isFlaggedFraud: 0,
    });

    setResult(null);
  };

  // =========================
  // ANALYZE TRANSACTION
  // =========================
  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setResult(null);

    try {
      // =========================
      // SEND DATA TO FASTAPI
      // =========================
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      // =========================
      // SERVER ERROR
      // =========================
      if (!response.ok || data.error) {
        throw new Error(
          data.error ||
            data.detail ||
            `Server error ${response.status}`
        );
      }

      // ==================================================
      // IMPORTANT SECURITY RULE
      // ==================================================
      //
      // If an existing fraud rule has already flagged
      // this transaction, it MUST be treated as FRAUD.
      //
      // This prevents the UI from showing SAFE when:
      // isFlaggedFraud = 1
      //
      const isRuleFlagged =
        Number(formData.isFlaggedFraud) === 1;

      // Backend ML prediction
      const backendPrediction =
        Number(data.prediction) === 1 ? 1 : 0;

      // Final prediction
      const finalPrediction =
        isRuleFlagged
          ? 1
          : backendPrediction;

      // =========================
      // FINAL RESULT
      // =========================
      const transactionResult =
        finalPrediction === 1
          ? "FRAUD"
          : "SAFE";

      // =========================
      // FINAL RISK
      // =========================
      let finalRisk = data.risk || "LOW";

      if (finalPrediction === 1) {
        finalRisk = "HIGH";
      } else {
        const fraudProbability =
          Number(data.fraud_probability) || 0;

        if (fraudProbability >= 50) {
          finalRisk = "HIGH";
        } else if (fraudProbability >= 20) {
          finalRisk = "MEDIUM";
        } else {
          finalRisk = "LOW";
        }
      }

      // =========================
      // PROBABILITIES
      // =========================
      let fraudProbability =
        Number(data.fraud_probability);

      let safeProbability =
        Number(data.safe_probability);

      // Handle invalid backend values
      if (
        Number.isNaN(fraudProbability) ||
        fraudProbability < 0
      ) {
        fraudProbability = 0;
      }

      if (
        Number.isNaN(safeProbability) ||
        safeProbability < 0
      ) {
        safeProbability = 100 - fraudProbability;
      }

      // Make sure percentages stay between 0-100
      fraudProbability = Math.min(
        Math.max(fraudProbability, 0),
        100
      );

      safeProbability = Math.min(
        Math.max(safeProbability, 0),
        100
      );

      // ==================================================
      // IF TRANSACTION IS FLAGGED
      // ==================================================
      //
      // We make the UI clearly show the security alert.
      //
      if (isRuleFlagged) {
        fraudProbability = Math.max(
          fraudProbability,
          90
        );

        safeProbability = 100 - fraudProbability;
      }

      // =========================
      // HISTORY ITEM
      // =========================
      const historyItem = {
        id: Date.now(),

        ...formData,

        result: transactionResult,

        // IMPORTANT:
        // Save final prediction, not raw backend prediction
        prediction: finalPrediction,

        risk: finalRisk,

        fraud_probability: fraudProbability,

        safe_probability: safeProbability,

        date: new Date().toLocaleString("en-IN"),
      };

      // =========================
      // SAVE HISTORY
      // =========================
      const oldHistory = JSON.parse(
        localStorage.getItem(
          "transactionHistory"
        ) || "[]"
      );

      localStorage.setItem(
        "transactionHistory",
        JSON.stringify([
          historyItem,
          ...oldHistory,
        ])
      );

      // =========================
      // SHOW RESULT
      // =========================
      setResult({
        success: true,

        result: transactionResult,

        prediction: finalPrediction,

        risk: finalRisk,

        fraud_probability:
          fraudProbability,

        safe_probability:
          safeProbability,

        isRuleFlagged,
      });
    } catch (error) {
      console.error(
        "Prediction error:",
        error
      );

      setResult({
        success: false,

        message:
          error.message ||
          "Unable to connect to prediction server.",
      });
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // FRAUD CHECK
  // =========================
  const isFraud =
    result?.success === true &&
    (
      result.result === "FRAUD" ||
      Number(result.prediction) === 1
    );

  return (
    <div className="analyze-page">

      {/* =========================
          NAVBAR
      ========================= */}

      <header className="analyze-header-bar">

        <Link
          to="/dashboard"
          className="analyze-brand"
        >
          <span>🛡️</span>
          Identity Guard
        </Link>

        <div className="analyze-nav">

          <Link to="/dashboard">
            Dashboard
          </Link>

          <Link to="/history">
            History
          </Link>

        </div>

      </header>


      <main className="analyze-main">

        {/* =========================
            PAGE HEADER
        ========================= */}

        <section className="analyze-title-section">

          <div className="analyze-status">

            <span className="status-dot"></span>

            AI FRAUD DETECTION ACTIVE

          </div>

          <h1>
            Analyze
            <span> Transaction</span>
          </h1>

          <p>
            Check a financial transaction using our
            AI-powered Random Forest fraud detection model.
          </p>

        </section>


        {/* =========================
            FORM + INFO
        ========================= */}

        <section className="analyze-layout">

          {/* =========================
              TRANSACTION FORM
          ========================= */}

          <div className="transaction-card">

            <div className="transaction-card-header">

              <div className="transaction-card-icon">
                💳
              </div>

              <div>

                <h2>
                  Transaction Details
                </h2>

                <p>
                  Enter the transaction information below
                </p>

              </div>

            </div>


            <form
              className="premium-form"
              onSubmit={handleSubmit}
            >

              {/* =========================
                  STEP
              ========================= */}

              <div className="input-group">

                <label>
                  Time Step
                </label>

                <input
                  type="number"
                  name="step"
                  value={formData.step}
                  onChange={handleChange}
                  min="1"
                  required
                />

              </div>


              {/* =========================
                  TYPE
              ========================= */}

              <div className="input-group">

                <label>
                  Transaction Type
                </label>

                <select
                  name="type"
                  value={formData.type}
                  onChange={handleChange}
                >

                  <option value="TRANSFER">
                    TRANSFER
                  </option>

                  <option value="CASH_OUT">
                    CASH_OUT
                  </option>

                  <option value="PAYMENT">
                    PAYMENT
                  </option>

                  <option value="CASH_IN">
                    CASH_IN
                  </option>

                  <option value="DEBIT">
                    DEBIT
                  </option>

                </select>

              </div>


              {/* =========================
                  AMOUNT
              ========================= */}

              <div className="input-group">

                <label>
                  Transaction Amount
                </label>

                <div className="input-with-icon">

                  <span>₹</span>

                  <input
                    type="number"
                    name="amount"
                    value={formData.amount}
                    onChange={handleChange}
                    min="0"
                    step="any"
                    required
                  />

                </div>

              </div>


              {/* =========================
                  SENDER
              ========================= */}

              <div className="form-section-title">
                <span>
                  Sender Information
                </span>
              </div>


              <div className="two-inputs">

                <div className="input-group">

                  <label>
                    Sender Old Balance
                  </label>

                  <input
                    type="number"
                    name="oldbalanceOrg"
                    value={formData.oldbalanceOrg}
                    onChange={handleChange}
                    min="0"
                    step="any"
                    required
                  />

                </div>


                <div className="input-group">

                  <label>
                    Sender New Balance
                  </label>

                  <input
                    type="number"
                    name="newbalanceOrig"
                    value={formData.newbalanceOrig}
                    onChange={handleChange}
                    min="0"
                    step="any"
                    required
                  />

                </div>

              </div>


              {/* =========================
                  RECEIVER
              ========================= */}

              <div className="form-section-title">
                <span>
                  Receiver Information
                </span>
              </div>


              <div className="two-inputs">

                <div className="input-group">

                  <label>
                    Receiver Old Balance
                  </label>

                  <input
                    type="number"
                    name="oldbalanceDest"
                    value={formData.oldbalanceDest}
                    onChange={handleChange}
                    min="0"
                    step="any"
                    required
                  />

                </div>


                <div className="input-group">

                  <label>
                    Receiver New Balance
                  </label>

                  <input
                    type="number"
                    name="newbalanceDest"
                    value={formData.newbalanceDest}
                    onChange={handleChange}
                    min="0"
                    step="any"
                    required
                  />

                </div>

              </div>


              {/* =========================
                  FRAUD FLAG
              ========================= */}

              <div className="input-group">

                <label>
                  Flagged by Existing Rule?
                </label>

                <select
                  name="isFlaggedFraud"
                  value={formData.isFlaggedFraud}
                  onChange={handleChange}
                >

                  <option value={0}>
                    No
                  </option>

                  <option value={1}>
                    Yes
                  </option>

                </select>

              </div>


              {/* =========================
                  BUTTONS
              ========================= */}

              <div className="analyze-actions">

                <button
                  type="submit"
                  className="analyze-submit"
                  disabled={loading}
                >

                  {loading
                    ? "🤖 AI Analyzing..."
                    : "🔍 Analyze Transaction"}

                </button>


                <button
                  type="button"
                  className="reset-button"
                  onClick={handleReset}
                  disabled={loading}
                >
                  ↻ Reset
                </button>

              </div>

            </form>

          </div>


          {/* =========================
              RIGHT INFO
          ========================= */}

          <aside className="analyze-info">

            <div className="info-card">

              <div className="info-icon">
                🤖
              </div>

              <span>
                AI MODEL
              </span>

              <h3>
                Random Forest
              </h3>

              <p>
                Your transaction is evaluated using
                our trained machine learning model.
              </p>


              <div className="info-line">

                <span>
                  Model Status
                </span>

                <strong>
                  <i></i> Active
                </strong>

              </div>


              <div className="info-line">

                <span>
                  Detection
                </span>

                <strong>
                  Real-time
                </strong>

              </div>

            </div>


            <div className="info-card protection-card">

              <div className="info-icon">
                🛡️
              </div>

              <span>
                SECURITY
              </span>

              <h3>
                Protected Analysis
              </h3>

              <p>
                Transaction details are processed by the
                prediction model to identify potentially
                fraudulent activity.
              </p>

            </div>

          </aside>

        </section>


        {/* =========================
            LOADING
        ========================= */}

        {loading && (

          <div className="analysis-loading">

            <div className="loading-orbit">
              🤖
            </div>

            <h2>
              AI is analyzing your transaction
            </h2>

            <p>
              Random Forest is checking
              transaction patterns...
            </p>

          </div>

        )}


        {/* =========================
            FRAUD / SAFE RESULT
        ========================= */}

        {!loading &&
          result?.success && (

            <section
              className={`analysis-result ${
                isFraud
                  ? "fraud-result"
                  : "safe-result"
              }`}
            >

              {/* =========================
                  RESULT TOP
              ========================= */}

              <div className="result-top">

                <div className="result-icon">

                  {isFraud
                    ? "🚨"
                    : "✅"}

                </div>


                <div>

                  <span className="result-label">

                    {isFraud
                      ? "SECURITY ALERT"
                      : "ANALYSIS COMPLETE"}

                  </span>


                  <h2>

                    {isFraud
                      ? "Fraudulent Transaction"
                      : "Transaction is Safe"}

                  </h2>


                  <p>

                    {isFraud
                      ? result.isRuleFlagged
                        ? "This transaction was flagged by an existing fraud rule and has been marked as HIGH RISK."
                        : "Suspicious financial activity was detected by the AI fraud detection system."
                      : "No significant fraudulent activity was detected."}

                  </p>

                </div>

              </div>


              {/* =========================
                  FRAUD WARNING
              ========================= */}

              {isFraud && (

                <div className="fraud-warning">

                  🚨

                  <div>

                    <strong>
                      FRAUD ALERT
                    </strong>

                    <span>
                      Transaction requires immediate attention.
                    </span>

                  </div>

                </div>

              )}


              {/* =========================
                  RESULT STATS
              ========================= */}

              <div className="result-stats">

                <div>

                  <span>
                    Risk Level
                  </span>

                  <strong>
                    {result.risk}
                  </strong>

                </div>


                <div>

                  <span>
                    Fraud Probability
                  </span>

                  <strong>
                    {result.fraud_probability}%
                  </strong>

                </div>


                <div>

                  <span>
                    Safe Probability
                  </span>

                  <strong>
                    {result.safe_probability}%
                  </strong>

                </div>


                <div>

                  <span>
                    Prediction
                  </span>

                  <strong>
                    {result.prediction}
                  </strong>

                </div>

              </div>


              {/* =========================
                  PROBABILITY BAR
              ========================= */}

              <div className="probability-bar">

                <div
                  style={{
                    width: `${Math.min(
                      Math.max(
                        Number(
                          result.fraud_probability
                        ) || 0,
                        0
                      ),
                      100
                    )}%`,
                  }}
                ></div>

              </div>


              {/* =========================
                  FOOTER
              ========================= */}

              <div className="result-footer">

                <span>
                  🤖 Random Forest ML Model
                </span>

                <Link to="/history">
                  View Analysis History →
                </Link>

              </div>

            </section>

          )}


        {/* =========================
            ERROR
        ========================= */}

        {!loading &&
          result?.success === false && (

            <section className="analysis-error">

              <div>
                ⚠️
              </div>

              <div>

                <h2>
                  Connection Error
                </h2>

                <p>
                  {result.message}
                </p>

                <small>
                  FastAPI: {API_URL}
                </small>

              </div>

            </section>

          )}

      </main>

    </div>
  );
}

export default Analyze;