import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function History() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const saved = JSON.parse(
      localStorage.getItem("transactionHistory") || "[]"
    );

    setTransactions(saved);
  }, []);

  const clearHistory = () => {
    const confirmClear = window.confirm(
      "Are you sure you want to clear all transaction history?"
    );

    if (!confirmClear) return;

    localStorage.removeItem("transactionHistory");
    setTransactions([]);
  };

  const fraudCount = transactions.filter(
    (item) => item.result === "FRAUD"
  ).length;

  const safeCount = transactions.filter(
    (item) => item.result === "SAFE"
  ).length;

  return (
    <div className="premium-history">

      {/* NAVBAR */}
      <header className="history-navbar">

        <Link to="/dashboard" className="history-logo">
          <span>🛡️</span>

          <div>
            <strong>Identity Guard</strong>
            <small>AI FRAUD PROTECTION</small>
          </div>
        </Link>

        <nav className="history-nav">

          <Link to="/dashboard">
            Dashboard
          </Link>

          <Link to="/analyze">
            Analyze
          </Link>

          <Link
            to="/history"
            className="history-nav-active"
          >
            History
          </Link>

        </nav>

        <Link
          to="/analyze"
          className="history-new-button"
        >
          + New Analysis
        </Link>

      </header>


      {/* MAIN */}
      <main className="history-content">

        {/* TITLE */}
        <section className="history-title">

          <div className="history-status">
            <span></span>
            TRANSACTION MONITORING
          </div>

          <h1>
            Transaction
            <span> History</span>
          </h1>

          <p>
            Review your previous fraud detection
            analyses and risk assessments.
          </p>

        </section>


        {/* STATS */}
        <section className="history-stat-grid">

          <div className="history-stat-card">

            <div className="history-stat-icon purple">
              📋
            </div>

            <div>
              <small>Total Analyses</small>
              <strong>{transactions.length}</strong>
            </div>

          </div>


          <div className="history-stat-card">

            <div className="history-stat-icon red">
              🚨
            </div>

            <div>
              <small>Fraud Detected</small>
              <strong>{fraudCount}</strong>
            </div>

          </div>


          <div className="history-stat-card">

            <div className="history-stat-icon green">
              🛡️
            </div>

            <div>
              <small>Safe Transactions</small>
              <strong>{safeCount}</strong>
            </div>

          </div>


          <div className="history-stat-card">

            <div className="history-stat-icon cyan">
              📈
            </div>

            <div>
              <small>Detection Rate</small>
              <strong>
                {transactions.length
                  ? Math.round(
                      (fraudCount /
                        transactions.length) *
                        100
                    )
                  : 0}
                %
              </strong>
            </div>

          </div>

        </section>


        {/* EMPTY */}
        {transactions.length === 0 && (

          <section className="history-empty">

            <div className="empty-icon">
              📭
            </div>

            <h2>
              No transactions yet
            </h2>

            <p>
              Analyze your first transaction and
              the result will appear here.
            </p>

            <Link
              to="/analyze"
              className="empty-action"
            >
              🔍 Start First Analysis
            </Link>

          </section>

        )}


        {/* HISTORY LIST */}
        {transactions.length > 0 && (

          <section className="history-panel">

            <div className="history-panel-header">

              <div>
                <span>
                  ANALYSIS RECORDS
                </span>

                <h2>
                  Recent Transactions
                </h2>
              </div>

              <button
                className="clear-history"
                onClick={clearHistory}
              >
                🗑 Clear History
              </button>

            </div>


            <div className="history-list">

              {transactions.map(
                (transaction, index) => {

                  const isFraud =
                    transaction.result === "FRAUD";

                  return (
                    <div
                      className="history-row"
                      key={
                        transaction.id || index
                      }
                    >

                      {/* ICON */}
                      <div
                        className={`history-result-icon ${
                          isFraud
                            ? "fraud"
                            : "safe"
                        }`}
                      >
                        {isFraud
                          ? "🚨"
                          : "✓"}
                      </div>


                      {/* DETAILS */}
                      <div className="history-details">

                        <div className="history-type-row">

                          <strong>
                            {transaction.type ||
                              "TRANSACTION"}
                          </strong>

                          <span
                            className={
                              isFraud
                                ? "result-fraud"
                                : "result-safe"
                            }
                          >
                            {transaction.result}
                          </span>

                        </div>

                        <p>
                          Transaction Amount:
                          {" "}
                          <strong>
                            ₹
                            {Number(
                              transaction.amount ||
                                0
                            ).toLocaleString(
                              "en-IN"
                            )}
                          </strong>
                        </p>

                        <small>
                          {transaction.date ||
                            "Date unavailable"}
                        </small>

                      </div>


                      {/* RISK */}
                      <div className="history-risk">

                        <span>
                          Risk
                        </span>

                        <strong
                          className={
                            transaction.risk ===
                            "HIGH"
                              ? "risk-high"
                              : transaction.risk ===
                                "MEDIUM"
                              ? "risk-medium"
                              : "risk-low"
                          }
                        >
                          {transaction.risk ||
                            "LOW"}
                        </strong>

                      </div>


                      {/* PROBABILITY */}
                      <div className="history-probability">

                        <strong>
                          {Number(
                            transaction.fraud_probability ||
                              0
                          ).toFixed(2)}
                          %
                        </strong>

                        <span>
                          Fraud Probability
                        </span>

                        <div className="mini-bar">
                          <div
                            style={{
                              width: `${Math.min(
                                Math.max(
                                  Number(
                                    transaction.fraud_probability ||
                                      0
                                  ),
                                  0
                                ),
                                100
                              )}%`,
                            }}
                          />
                        </div>

                      </div>

                    </div>
                  );
                }
              )}

            </div>

          </section>

        )}


        {/* SECURITY FOOTER */}
        <section className="history-security">

          <div className="history-security-icon">
            🛡️
          </div>

          <div>

            <span>
              IDENTITY GUARD SECURITY
            </span>

            <h3>
              Your analysis history is stored locally
            </h3>

            <p>
              Transaction results shown here are
              saved in your browser for this session.
            </p>

          </div>

        </section>


      </main>

    </div>
  );
}

export default History;