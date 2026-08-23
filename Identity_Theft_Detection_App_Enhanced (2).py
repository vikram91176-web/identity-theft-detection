import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
from pathlib import Path
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Identity Guard | Identity Theft Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL_PATH = Path("identity_theft_random_forest.pkl")

# =========================================================
# PROJECT METRICS
# These values are taken from the completed PaySim experiment.
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
# CUSTOM CSS
# =========================================================
st.markdown(
    """
<style>
.stApp {
    background: #07111f;
    color: #eef5ff;
}

[data-testid="stSidebar"] {
    background: #0b1728;
    border-right: 1px solid #1e3553;
}

.hero {
    padding: 30px 32px;
    border-radius: 22px;
    background: linear-gradient(135deg, #102744, #0a1627);
    border: 1px solid #234a73;
    margin-bottom: 22px;
    box-shadow: 0 10px 35px rgba(0,0,0,.20);
}

.hero h1 {
    margin: 0;
    font-size: 40px;
    color: #f5f9ff;
}

.hero p {
    margin: 9px 0 0;
    color: #a9c0da;
    font-size: 16px;
}

.metric-card {
    padding: 20px 16px;
    min-height: 118px;
    border-radius: 17px;
    background: #0d1c30;
    border: 1px solid #203b5b;
    text-align: center;
    transition: transform .2s ease, border-color .2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    border-color: #4b9cff;
}

.metric-title {
    color: #8fa8c4;
    font-size: 13px;
}

.metric-value {
    color: #f5f9ff;
    font-size: 30px;
    font-weight: 800;
    margin-top: 7px;
}

.result-safe, .result-danger {
    padding: 28px;
    border-radius: 20px;
    text-align: center;
    margin-top: 18px;
    animation: resultIn .55s ease-out;
}

.result-safe {
    background: linear-gradient(135deg, #0d2a20, #0a1e18);
    border: 1px solid #287354;
    box-shadow: 0 0 30px rgba(40,115,84,.18);
}

.result-danger {
    background: linear-gradient(135deg, #35151c, #241019);
    border: 1px solid #d44c62;
    box-shadow: 0 0 35px rgba(212,76,98,.22);
    animation: resultIn .55s ease-out, dangerPulse 1.8s infinite;
}

.result-title {
    font-size: 30px;
    font-weight: 850;
}

.result-sub {
    color: #b8c9db;
    margin-top: 9px;
    font-size: 16px;
}

.scan-box {
    padding: 28px;
    border-radius: 20px;
    background: #0b1b2f;
    border: 1px solid #28517b;
    text-align: center;
    margin: 18px 0;
}

.scan-icon {
    font-size: 42px;
    animation: scanPulse 1s infinite;
}

.scan-title {
    font-size: 22px;
    font-weight: 800;
    margin-top: 8px;
}

.scan-line {
    width: 72%;
    height: 5px;
    margin: 18px auto 8px;
    border-radius: 99px;
    background: linear-gradient(90deg, #1d7cff, #6ec8ff, #1d7cff);
    background-size: 200% 100%;
    animation: scanMove 1.2s linear infinite;
}

.risk-wrap {
    margin-top: 20px;
    padding: 20px;
    border-radius: 18px;
    background: #0d1c30;
    border: 1px solid #203b5b;
}

.risk-label {
    display: flex;
    justify-content: space-between;
    color: #a9c0da;
    margin-bottom: 10px;
}

.risk-track {
    height: 13px;
    border-radius: 99px;
    background: #182b43;
    overflow: hidden;
}

.risk-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #29c46a, #f0c419, #ef4b5f);
    box-shadow: 0 0 14px rgba(75,156,255,.25);
}

.workflow-card {
    padding: 20px;
    border-radius: 17px;
    background: #0d1c30;
    border: 1px solid #203b5b;
    height: 100%;
}

.workflow-number {
    display: inline-flex;
    width: 34px;
    height: 34px;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #173a61;
    color: #8bc5ff;
    font-weight: 800;
}

.model-badge {
    display: inline-block;
    padding: 8px 13px;
    border-radius: 999px;
    background: #12355a;
    border: 1px solid #28649c;
    color: #b9ddff;
    margin: 4px;
}

.footer-note {
    color: #7188a2;
    font-size: 12px;
    text-align: center;
    padding: 24px 0 8px;
}

@keyframes scanPulse {
    0%,100% { transform: scale(1); opacity: .75; }
    50% { transform: scale(1.18); opacity: 1; }
}

@keyframes scanMove {
    0% { background-position: 0% 0%; }
    100% { background-position: 200% 0%; }
}

@keyframes resultIn {
    from { opacity: 0; transform: translateY(12px) scale(.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes dangerPulse {
    0%,100% { box-shadow: 0 0 25px rgba(212,76,98,.18); }
    50% { box-shadow: 0 0 42px rgba(212,76,98,.35); }
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 48px;
    font-weight: 800;
}

div[data-testid="stMetric"] {
    background: #0d1c30;
    border: 1px solid #203b5b;
    padding: 12px;
    border-radius: 15px;
}
</style>
""",
    unsafe_allow_html=True,
)

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
    st.markdown("**Model:** Random Forest")
    st.markdown("**Dataset:** PaySim")
    st.markdown("**Training sample:** 1,000,000 transactions")

# =========================================================
# DASHBOARD
# =========================================================
if page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>🛡️ Identity Theft Detection</h1>
            <p>Detect suspicious financial transactions using machine learning.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    for col, title, value in [
        (c1, "Accuracy", "99.97%"),
        (c2, "Precision", "78.41%"),
        (c3, "Recall", "64.49%"),
        (c4, "F1 Score", "70.77%"),
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
        st.subheader("📊 Random Forest Performance")
        chart_df = pd.DataFrame(
            {"Score (%)": list(METRICS.values())},
            index=list(METRICS.keys()),
        )
        st.bar_chart(chart_df, height=330)

    with right:
        st.subheader("💳 PaySim Dataset")
        st.metric("Transactions analyzed", f"{DATASET_ROWS:,}")
        st.metric("Fraudulent transactions", f"{DATASET_FRAUD:,}")
        st.metric("Fraud rate", f"{DATASET_FRAUD / DATASET_ROWS * 100:.3f}%")

    st.write("")
    st.subheader("🔄 Detection Workflow")

    w1, w2, w3, w4 = st.columns(4)

    workflow = [
        ("1", "Transaction", "User enters transaction details"),
        ("2", "Preprocessing", "Features are prepared for ML"),
        ("3", "Random Forest", "Trained model predicts risk"),
        ("4", "Risk Decision", "Probability becomes a risk level"),
    ]

    for col, (num, title, desc) in zip([w1, w2, w3, w4], workflow):
        with col:
            st.markdown(
                f"""
                <div class="workflow-card">
                    <span class="workflow-number">{num}</span>
                    <h4>{title}</h4>
                    <p class="small-note">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# =========================================================
# ANALYZE TRANSACTION
# =========================================================
elif page == "Analyze Transaction":

    st.markdown(
        """
        <div class="hero">
            <h1>🔍 Analyze Transaction</h1>
            <p>Enter transaction details and let the trained Random Forest model assess the risk.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if model is None:
        st.error(
            "Model file not found. Put 'identity_theft_random_forest.pkl' "
            "in the same folder as app.py."
        )
        st.stop()

    with st.form("transaction_form"):

        c1, c2 = st.columns(2)

        with c1:
            step = st.number_input("Time Step", min_value=1, value=1)
            amount = st.number_input(
                "Transaction Amount",
                min_value=0.0,
                value=1000.0,
            )
            oldbalance_org = st.number_input(
                "Sender Old Balance",
                min_value=0.0,
                value=5000.0,
            )
            newbalance_orig = st.number_input(
                "Sender New Balance",
                min_value=0.0,
                value=4000.0,
            )

        with c2:
            transaction_type = st.selectbox(
                "Transaction Type",
                TRANSACTION_TYPES,
            )
            oldbalance_dest = st.number_input(
                "Receiver Old Balance",
                min_value=0.0,
                value=1000.0,
            )
            newbalance_dest = st.number_input(
                "Receiver New Balance",
                min_value=0.0,
                value=2000.0,
            )
            flagged = st.selectbox(
                "Flagged by Existing Rule?",
                [0, 1],
            )

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

        # CASH_IN is the reference category, so all type columns stay 0.
        if transaction_type != "CASH_IN":
            key = f"type_{transaction_type}"
            if key in row:
                row[key] = 1

        input_df = pd.DataFrame([row], columns=FEATURES)

        # -----------------------------
        # Animated AI scanning
        # -----------------------------
        scan_placeholder = st.empty()

        scan_placeholder.markdown(
            """
            <div class="scan-box">
                <div class="scan-icon">🤖</div>
                <div class="scan-title">AI SCANNING TRANSACTION...</div>
                <div class="scan-line"></div>
                <div class="small-note">
                    Checking transaction pattern → balances → fraud indicators
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        time.sleep(.8)

        scan_placeholder.markdown(
            """
            <div class="scan-box">
                <div class="scan-icon">🔎</div>
                <div class="scan-title">ANALYZING BEHAVIOR PATTERNS...</div>
                <div class="scan-line"></div>
                <div class="small-note">
                    Random Forest is evaluating the transaction
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        time.sleep(.8)

        prediction = int(model.predict(input_df)[0])

        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(input_df)[0][1])
        else:
            probability = float(prediction)

        probability = min(max(probability, 0.0), 1.0)

        scan_placeholder.empty()

        if prediction == 1:
            risk = "HIGH"
            title = "🚨 FRAUDULENT TRANSACTION"
            box_class = "result-danger"
        else:
            risk = "LOW"
            title = "✅ NORMAL TRANSACTION"
            box_class = "result-safe"

        st.markdown(
            f"""
            <div class="{box_class}">
                <div class="result-title">{title}</div>
                <div class="result-sub">
                    Risk Level: <strong>{risk}</strong>
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    Fraud Probability: <strong>{probability * 100:.2f}%</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Animated-style risk meter
        pct = probability * 100
        st.markdown(
            f"""
            <div class="risk-wrap">
                <div class="risk-label">
                    <span>🎯 Risk Score</span>
                    <strong>{pct:.2f}%</strong>
                </div>
                <div class="risk-track">
                    <div class="risk-fill" style="width:{pct:.2f}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric("Prediction", "FRAUD" if prediction else "NORMAL")

        with r2:
            st.metric("Risk Level", risk)

        with r3:
            st.metric("Fraud Probability", f"{pct:.2f}%")

        # Save history
        st.session_state.history.insert(
            0,
            {
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Time Step": step,
                "Type": transaction_type,
                "Amount": round(amount, 2),
                "Prediction": "FRAUD" if prediction else "NORMAL",
                "Risk": risk,
                "Fraud Probability": f"{pct:.2f}%",
            },
        )

        st.session_state.last_result = {
            "prediction": prediction,
            "probability": probability,
            "risk": risk,
        }

        st.success("Transaction analysis completed and saved to history.")

# =========================================================
# TRANSACTION HISTORY
# =========================================================
elif page == "Transaction History":

    st.markdown(
        """
        <div class="hero">
            <h1>📋 Transaction History</h1>
            <p>Transactions analyzed during this application session.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.history:
        st.info("No transactions analyzed yet. Go to Analyze Transaction.")
    else:
        history_df = pd.DataFrame(st.session_state.history)

        total = len(history_df)
        frauds = int((history_df["Prediction"] == "FRAUD").sum())
        normal = total - frauds

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Analyzed", total)
        c2.metric("Fraud Detected", frauds)
        c3.metric("Normal", normal)

        st.write("")
        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

# =========================================================
# MODEL PERFORMANCE
# =========================================================
elif page == "Model Performance":

    st.markdown(
        """
        <div class="hero">
            <h1>📈 Model Performance</h1>
            <p>Evaluation results from the completed PaySim machine-learning experiment.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🏆 Final Random Forest Metrics")

    c1, c2, c3, c4 = st.columns(4)

    for col, (name, value) in zip(c1.columns if False else [c1,c2,c3,c4], METRICS.items()):
        with col:
            st.metric(name, f"{value:.2f}%")

    st.write("")
    st.bar_chart(
        pd.DataFrame(
            {"Score (%)": list(METRICS.values())},
            index=list(METRICS.keys()),
        ),
        height=350,
    )

    st.subheader("🧩 Confusion Matrix")

    cm1, cm2 = st.columns([1, 1])

    with cm1:
        cm_df = pd.DataFrame(
            CONFUSION_MATRIX,
            index=["Actual Normal", "Actual Fraud"],
            columns=["Predicted Normal", "Predicted Fraud"],
        )
        st.dataframe(cm_df, use_container_width=True)

    with cm2:
        st.markdown(
            """
            <div class="workflow-card">
                <h3>What it means</h3>
                <p>🟢 True Negative: Normal transaction correctly identified.</p>
                <p>🔵 True Positive: Fraud transaction correctly identified.</p>
                <p>🟠 False Positive: Normal transaction flagged as fraud.</p>
                <p>🔴 False Negative: Fraud transaction missed by the model.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("🤖 Models Evaluated")

    for name in [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "XGBoost",
    ]:
        st.markdown(
            f'<span class="model-badge">{name}</span>',
            unsafe_allow_html=True,
        )

    st.success(
        "Random Forest is the final model used by this application. "
        "Its reported F1 Score is 70.77%."
    )

# =========================================================
# ABOUT MODEL
# =========================================================
elif page == "About Model":

    st.markdown(
        """
        <div class="hero">
            <h1>🤖 About the Project</h1>
            <p>Machine-learning based fraudulent transaction risk detection using PaySim.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Project Objective")
    st.write(
        "The application analyzes financial transaction features and predicts "
        "whether a transaction appears fraudulent."
    )

    st.subheader("Technology Stack")

    tech1, tech2, tech3, tech4 = st.columns(4)

    tech1.info("🐍 Python")
    tech2.info("🧠 Scikit-learn")
    tech3.info("🌲 Random Forest")
    tech4.info("📊 Streamlit")

    st.subheader("Dataset")
    st.write(
        f"PaySim dataset with {DATASET_ROWS:,} transactions used in the completed experiment."
    )

    st.subheader("Models Evaluated")
    st.write(
        "Logistic Regression, Decision Tree, Random Forest and XGBoost."
    )

    st.subheader("Final Model")
    st.success(
        "Random Forest was selected as the final model because it achieved "
        "the highest F1-score in the completed experiment."
    )

    st.subheader("Important Project Note")
    st.warning(
        "PaySim provides a fraud label, not a direct identity-theft label. "
        "This application therefore treats fraudulent transactions as "
        "potential indicators of unauthorized activity or identity-theft risk."
    )

    st.subheader("Model Performance")
    st.dataframe(
        pd.DataFrame([METRICS]),
        use_container_width=True,
        hide_index=True,
    )

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer-note">
        Identity Guard • Identity Theft Detection • PaySim • Random Forest
    </div>
    """,
    unsafe_allow_html=True,
)
