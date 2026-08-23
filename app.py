import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Identity Guard | Identity Theft Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "identity_theft_random_forest.pkl"

# =========================================================
# PROJECT RESULTS FROM YOUR COMPLETED PAYSim EXPERIMENT
# =========================================================
METRICS = {
    "Accuracy": 99.97,
    "Precision": 78.41,
    "Recall": 64.49,
    "F1 Score": 70.77,
}

CONFUSION_MATRIX = np.array([
    [199874, 19],
    [38, 69],
])

DATASET_ROWS = 1_000_000
DATASET_FRAUD = 535

FEATURES = [
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "isFlaggedFraud",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]

TRANSACTION_TYPES = ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]

# =========================================================
# CSS / ANIMATIONS
# =========================================================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 85% 5%, rgba(35, 115, 190, .16), transparent 28%),
        #07111f;
    color: #eef5ff;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1729, #07111f);
    border-right: 1px solid #203a5c;
}

.hero {
    padding: 32px;
    border-radius: 24px;
    background: linear-gradient(135deg, #102c4d, #0a1627);
    border: 1px solid #28557f;
    box-shadow: 0 12px 35px rgba(0,0,0,.20);
    margin-bottom: 24px;
    animation: fadeUp .65s ease-out;
}

.hero h1 {
    margin: 0;
    font-size: 40px;
    color: #f7fbff;
}

.hero p {
    margin: 10px 0 0;
    color: #aac1da;
    font-size: 17px;
}

.metric-card {
    padding: 22px 15px;
    border-radius: 18px;
    background: rgba(13, 28, 48, .92);
    border: 1px solid #244463;
    text-align: center;
    transition: transform .25s ease, border-color .25s ease;
    animation: fadeUp .7s ease-out;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: #4d91cc;
}

.metric-title {
    color: #91a9c3;
    font-size: 14px;
}

.metric-value {
    color: #f7fbff;
    font-size: 30px;
    font-weight: 800;
    margin-top: 6px;
}

.section-card {
    padding: 22px;
    border-radius: 18px;
    background: rgba(10, 24, 41, .78);
    border: 1px solid #1d3b5b;
    margin-bottom: 18px;
}

.result-safe {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0b3023, #092019);
    border: 1px solid #319268;
    text-align: center;
    animation: resultPop .55s ease-out;
    box-shadow: 0 0 35px rgba(49,146,104,.12);
}

.result-danger {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #42151f, #241018);
    border: 1px solid #c94b63;
    text-align: center;
    animation: resultPop .55s ease-out, dangerPulse 1.5s ease-in-out 2;
    box-shadow: 0 0 35px rgba(201,75,99,.14);
}

.result-title {
    font-size: 30px;
    font-weight: 850;
}

.result-sub {
    color: #c1d0df;
    margin-top: 10px;
    font-size: 16px;
}

.scan-box {
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #28618d;
    background: linear-gradient(135deg, #0d2742, #091726);
    text-align: center;
    animation: scanGlow 1.2s infinite alternate;
}

.scan-ring {
    width: 54px;
    height: 54px;
    margin: 0 auto 12px;
    border: 5px solid #214766;
    border-top-color: #55b7ff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

.status-pill {
    display: inline-block;
    padding: 6px 13px;
    border-radius: 999px;
    background: #102e4b;
    border: 1px solid #2e6793;
    color: #bfe3ff;
    font-size: 13px;
    font-weight: 700;
}

.workflow {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}

.workflow-step {
    padding: 11px 15px;
    border-radius: 12px;
    background: #0d2035;
    border: 1px solid #254a6b;
    color: #c8d8e8;
    font-size: 14px;
}

.arrow {
    color: #55b7ff;
    font-weight: 800;
}

div.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 13px;
    font-weight: 800;
    border: 1px solid #3474a5;
    transition: transform .2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes resultPop {
    0% { opacity: 0; transform: scale(.96) translateY(8px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes dangerPulse {
    0%, 100% { box-shadow: 0 0 15px rgba(201,75,99,.08); }
    50% { box-shadow: 0 0 35px rgba(201,75,99,.28); }
}

@keyframes scanGlow {
    from { box-shadow: 0 0 8px rgba(85,183,255,.08); }
    to { box-shadow: 0 0 30px rgba(85,183,255,.20); }
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MODEL
# =========================================================
@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

# =========================================================
# SESSION STATE
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🛡️ Identity Guard")
    st.caption("AI-powered fraudulent transaction risk detector")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Analyze Transaction",
            "Transaction History",
            "Model Performance",
            "About Model",
        ],
    )

    st.divider()
    st.markdown("**Final Model:** Random Forest")
    st.markdown("**Dataset:** PaySim")
    st.markdown("**Training sample:** 1,000,000 transactions")

    if model is not None:
        st.success("Model loaded")
    else:
        st.error("Model file not found")

# =========================================================
# DASHBOARD
# =========================================================
if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <span class="status-pill">● SYSTEM READY</span>
        <h1>🛡️ Identity Theft Detection</h1>
        <p>Detect suspicious financial transactions using machine learning.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for col, title, value in [
        (cols[0], "Accuracy", "99.97%"),
        (cols[1], "Precision", "78.41%"),
        (cols[2], "Recall", "64.49%"),
        (cols[3], "F1 Score", "70.77%"),
    ]:
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    left, right = st.columns([1.15, .85])

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📊 Model Performance")
        chart_df = pd.DataFrame(
            {"Score (%)": list(METRICS.values())},
            index=list(METRICS.keys()),
        )
        st.bar_chart(chart_df, height=310)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📦 PaySim Dataset")
        st.metric("Transactions analyzed", f"{DATASET_ROWS:,}")
        st.metric("Fraudulent transactions", f"{DATASET_FRAUD:,}")
        st.metric("Fraud rate", f"{DATASET_FRAUD / DATASET_ROWS * 100:.3f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("🔄 Detection Workflow")
    st.markdown("""
    <div class="workflow">
        <div class="workflow-step">💳 Transaction</div>
        <div class="arrow">→</div>
        <div class="workflow-step">⚙️ Preprocessing</div>
        <div class="arrow">→</div>
        <div class="workflow-step">🌲 Random Forest</div>
        <div class="arrow">→</div>
        <div class="workflow-step">📈 Probability</div>
        <div class="arrow">→</div>
        <div class="workflow-step">🚨 Risk Decision</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# ANALYZE TRANSACTION
# =========================================================
elif page == "Analyze Transaction":
    st.markdown("""
    <div class="hero">
        <span class="status-pill">● LIVE ANALYSIS</span>
        <h1>🔍 Analyze Transaction</h1>
        <p>Enter transaction details and let the trained Random Forest model assess the risk.</p>
    </div>
    """, unsafe_allow_html=True)

    if model is None:
        st.error("Model file not found. Keep identity_theft_random_forest.pkl beside app.py.")
        st.stop()

    with st.form("transaction_form"):
        c1, c2 = st.columns(2)

        with c1:
            step = st.number_input("Time Step", min_value=1, value=1)
            amount = st.number_input("Transaction Amount", min_value=0.0, value=181.0)
            oldbalance_org = st.number_input("Sender Old Balance", min_value=0.0, value=181.0)
            newbalance_orig = st.number_input("Sender New Balance", min_value=0.0, value=0.0)

        with c2:
            transaction_type = st.selectbox("Transaction Type", TRANSACTION_TYPES)
            oldbalance_dest = st.number_input("Receiver Old Balance", min_value=0.0, value=0.0)
            newbalance_dest = st.number_input("Receiver New Balance", min_value=0.0, value=0.0)
            flagged = st.selectbox("Flagged by Existing Rule?", [0, 1])

        submitted = st.form_submit_button("🚀 ANALYZE TRANSACTION")

    if submitted:
        row = {
            "step": step,
            "amount": amount,
            "oldbalanceOrg": oldbalance_org,
            "newbalanceOrig": newbalance_orig,
            "oldbalanceDest": oldbalance_dest,
            "newbalanceDest": newbalance_dest,
            "isFlaggedFraud": flagged,
            "type_CASH_OUT": 0,
            "type_DEBIT": 0,
            "type_PAYMENT": 0,
            "type_TRANSFER": 0,
        }

        if transaction_type != "CASH_IN":
            key = f"type_{transaction_type}"
            if key in row:
                row[key] = 1

        input_df = pd.DataFrame([row], columns=FEATURES)

        # Animated AI scan
        scan_placeholder = st.empty()
        progress_placeholder = st.empty()

        scan_placeholder.markdown("""
        <div class="scan-box">
            <div class="scan-ring"></div>
            <h3>🤖 AI SCANNING TRANSACTION...</h3>
            <p>Checking transaction patterns, balances and fraud indicators</p>
        </div>
        """, unsafe_allow_html=True)

        for value in [15, 35, 55, 75, 90, 100]:
            progress_placeholder.progress(value)
            time.sleep(0.16)

        prediction = int(model.predict(input_df)[0])

        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(input_df)[0][1])
        else:
            probability = float(prediction)

        scan_placeholder.empty()
        progress_placeholder.empty()

        if prediction == 1:
            risk = "HIGH"
            title = "🚨 FRAUDULENT TRANSACTION"
            box_class = "result-danger"
            icon_message = "⚠️ Immediate attention recommended"
        else:
            risk = "LOW"
            title = "✅ NORMAL TRANSACTION"
            box_class = "result-safe"
            icon_message = "✓ No fraud signal detected"

        st.session_state.last_result = {
            "prediction": prediction,
            "probability": probability,
            "risk": risk,
        }

        st.markdown(
            f"""
            <div class="{box_class}">
                <div class="result-title">{title}</div>
                <div class="result-sub">
                    Risk Level: <strong>{risk}</strong>
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    Fraud Probability: <strong>{probability * 100:.2f}%</strong>
                </div>
                <div class="result-sub">{icon_message}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        st.progress(min(max(probability, 0.0), 1.0))

        r1, r2, r3 = st.columns(3)
        r1.metric("Prediction", "FRAUD" if prediction else "NORMAL")
        r2.metric("Risk Level", risk)
        r3.metric("Fraud Probability", f"{probability * 100:.2f}%")

        st.session_state.history.insert(
            0,
            {
                "Time Step": step,
                "Type": transaction_type,
                "Amount": amount,
                "Prediction": "FRAUD" if prediction else "NORMAL",
                "Risk": risk,
                "Fraud Probability": f"{probability * 100:.2f}%",
            },
        )

# =========================================================
# TRANSACTION HISTORY
# =========================================================
elif page == "Transaction History":
    st.markdown("""
    <div class="hero">
        <span class="status-pill">● SESSION LOG</span>
        <h1>📋 Transaction History</h1>
        <p>Recent transactions analyzed during this application session.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("No transactions analyzed yet. Go to Analyze Transaction to start.")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

# =========================================================
# MODEL PERFORMANCE
# =========================================================
elif page == "Model Performance":
    st.markdown("""
    <div class="hero">
        <span class="status-pill">● MODEL ANALYTICS</span>
        <h1>📈 Model Performance</h1>
        <p>Evaluation results from the completed PaySim experiment.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for col, title, value in [
        (cols[0], "Accuracy", "99.97%"),
        (cols[1], "Precision", "78.41%"),
        (cols[2], "Recall", "64.49%"),
        (cols[3], "F1 Score", "70.77%"),
    ]:
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    left, right = st.columns(2)

    with left:
        st.subheader("📊 Accuracy / Precision / Recall / F1")
        perf_df = pd.DataFrame({"Score (%)": METRICS})
        st.bar_chart(perf_df, height=330)

    with right:
        st.subheader("🧩 Confusion Matrix")
        cm_df = pd.DataFrame(
            CONFUSION_MATRIX,
            index=["Actual Normal", "Actual Fraud"],
            columns=["Predicted Normal", "Predicted Fraud"],
        )
        st.dataframe(cm_df, use_container_width=True)

        tn, fp = CONFUSION_MATRIX[0]
        fn, tp = CONFUSION_MATRIX[1]
        st.caption(
            f"TN: {tn:,}  |  FP: {fp:,}  |  FN: {fn:,}  |  TP: {tp:,}"
        )

    st.subheader("🌲 Final Model")
    st.success(
        "Random Forest was selected as the final model for this application "
        "based on the completed experiment."
    )

# =========================================================
# ABOUT MODEL
# =========================================================
elif page == "About Model":
    st.markdown("""
    <div class="hero">
        <span class="status-pill">● PROJECT INFORMATION</span>
        <h1>🤖 About the Model</h1>
        <p>Machine learning pipeline used for the Identity Theft Detection project.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Models Evaluated")
    st.write("Logistic Regression, Decision Tree, Random Forest and XGBoost.")

    st.subheader("Final Model")
    st.success("🌲 Random Forest")

    st.subheader("Dataset")
    st.write("PaySim — 1,000,000 transaction records used in the completed experiment.")

    st.subheader("Final Performance")
    st.dataframe(
        pd.DataFrame([METRICS]),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Important Project Note")
    st.warning(
        "PaySim provides a fraud label, not a direct identity-theft label. "
        "This application therefore treats fraudulent transactions as "
        "potential indicators of unauthorized activity or identity-theft risk."
    )
