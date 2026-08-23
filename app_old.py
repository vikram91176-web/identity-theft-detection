
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
from pathlib import Path

st.set_page_config(
    page_title="Identity Theft Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL_PATH = Path("identity_theft_random_forest.pkl")

# -----------------------------
# Demo / experiment metrics
# Based on the user's completed 1M-row PaySim experiment.
# -----------------------------
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

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
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
        padding: 28px 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, #102744, #0a1627);
        border: 1px solid #234a73;
        margin-bottom: 22px;
    }

    .hero h1 {
        margin: 0;
        font-size: 38px;
        color: #f5f9ff;
    }

    .hero p {
        margin: 8px 0 0;
        color: #a9c0da;
        font-size: 16px;
    }

    .metric-card {
        padding: 18px;
        border-radius: 16px;
        background: #0d1c30;
        border: 1px solid #203b5b;
        text-align: center;
    }

    .metric-title {
        color: #8fa8c4;
        font-size: 13px;
    }

    .metric-value {
        color: #f5f9ff;
        font-size: 28px;
        font-weight: 700;
        margin-top: 5px;
    }

    .result-safe {
        padding: 26px;
        border-radius: 18px;
        background: #0d2a20;
        border: 1px solid #287354;
        text-align: center;
    }

    .result-danger {
        padding: 26px;
        border-radius: 18px;
        background: #35151c;
        border: 1px solid #a43a4d;
        text-align: center;
    }

    .result-title {
        font-size: 28px;
        font-weight: 800;
    }

    .result-sub {
        color: #b8c9db;
        margin-top: 8px;
    }

    .small-note {
        color: #8fa8c4;
        font-size: 13px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 48px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Model loading
# -----------------------------
@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

# -----------------------------
# Session history
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## 🛡️ Identity Guard")
    st.caption("AI-powered fraudulent transaction risk detector")
    st.divider()

    page = st.radio(
        "Navigation",
        ["Dashboard", "Analyze Transaction", "Transaction History", "About Model"],
    )

    st.divider()
    st.markdown("**Model:** Random Forest")
    st.markdown("**Dataset:** PaySim")
    st.markdown("**Training sample:** 1,000,000 transactions")

# -----------------------------
# Dashboard
# -----------------------------
if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <h1>🛡️ Identity Theft Detection</h1>
        <p>Detect suspicious financial transactions using machine learning.</p>
    </div>
    """, unsafe_allow_html=True)

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
    left, right = st.columns([1.15, 0.85])

    with left:
        st.subheader("Model Performance")
        chart_df = pd.DataFrame(
            {"Score (%)": list(METRICS.values())},
            index=list(METRICS.keys()),
        )
        st.bar_chart(chart_df)

    with right:
        st.subheader("PaySim Dataset")
        st.metric("Transactions analyzed", f"{DATASET_ROWS:,}")
        st.metric("Fraudulent transactions", f"{DATASET_FRAUD:,}")
        st.metric("Fraud rate", f"{DATASET_FRAUD / DATASET_ROWS * 100:.3f}%")

    st.subheader("Detection Workflow")
    st.info(
        "PaySim transaction → preprocessing → Random Forest → "
        "fraud probability → risk classification"
    )

# -----------------------------
# Analyze Transaction
# -----------------------------
elif page == "Analyze Transaction":
    st.markdown("""
    <div class="hero">
        <h1>🔍 Analyze Transaction</h1>
        <p>Enter transaction details and let the trained Random Forest model assess the risk.</p>
    </div>
    """, unsafe_allow_html=True)

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
            amount = st.number_input("Transaction Amount", min_value=0.0, value=1000.0)
            oldbalance_org = st.number_input("Sender Old Balance", min_value=0.0, value=5000.0)
            newbalance_orig = st.number_input("Sender New Balance", min_value=0.0, value=4000.0)

        with c2:
            transaction_type = st.selectbox("Transaction Type", TRANSACTION_TYPES)
            oldbalance_dest = st.number_input("Receiver Old Balance", min_value=0.0, value=1000.0)
            newbalance_dest = st.number_input("Receiver New Balance", min_value=0.0, value=2000.0)
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

        with st.spinner("🤖 AI is analyzing transaction patterns..."):
            time.sleep(1.2)
            prediction = int(model.predict(input_df)[0])

            if hasattr(model, "predict_proba"):
                probability = float(model.predict_proba(input_df)[0][1])
            else:
                probability = float(prediction)

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

        st.progress(min(max(probability, 0.0), 1.0))

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

# -----------------------------
# History
# -----------------------------
elif page == "Transaction History":
    st.markdown("""
    <div class="hero">
        <h1>📋 Transaction History</h1>
        <p>Recent transactions analyzed during this application session.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("No transactions analyzed yet.")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

# -----------------------------
# About Model
# -----------------------------
elif page == "About Model":
    st.markdown("""
    <div class="hero">
        <h1>🤖 Model Information</h1>
        <p>Machine learning experiment used for the final application.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Models Evaluated")
    st.write(
        "Logistic Regression, Decision Tree, Random Forest and XGBoost."
    )

    st.subheader("Final Model")
    st.success(
        "Random Forest was selected because it achieved the highest F1-score "
        "in the completed experiment."
    )

    st.subheader("Final Performance")
    st.dataframe(
        pd.DataFrame([METRICS]),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Confusion Matrix")
    cm_df = pd.DataFrame(
        CONFUSION_MATRIX,
        index=["Actual Normal", "Actual Fraud"],
        columns=["Predicted Normal", "Predicted Fraud"],
    )
    st.dataframe(cm_df, use_container_width=True)

    st.subheader("Important Project Note")
    st.warning(
        "PaySim provides a fraud label, not a direct identity-theft label. "
        "This application therefore treats fraudulent transactions as "
        "potential indicators of unauthorized activity or identity-theft risk."
    )
