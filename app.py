from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import joblib

# =========================================================
# APP
# =========================================================

app = FastAPI(title="Identity Guard API")


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# MODEL
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "identity_theft_random_forest.pkl"

model = None

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Random Forest model loaded")
except Exception as e:
    print("❌ Model loading failed:", e)


# =========================================================
# FEATURES
# =========================================================

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


# =========================================================
# REQUEST MODEL
# =========================================================

class Transaction(BaseModel):

    step: int
    type: str

    amount: float

    oldbalanceOrg: float
    newbalanceOrig: float

    oldbalanceDest: float
    newbalanceDest: float

    isFlaggedFraud: int


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "message": "Identity Guard API is running"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


# =========================================================
# PREDICT
# =========================================================

@app.post("/predict")
def predict(transaction: Transaction):

    if model is None:

        return {
            "error": "Random Forest model could not be loaded."
        }


    # -----------------------------------------------------
    # CREATE INPUT
    # -----------------------------------------------------

    row = {

        "step": transaction.step,

        "amount": transaction.amount,

        "oldbalanceOrg": transaction.oldbalanceOrg,

        "newbalanceOrig": transaction.newbalanceOrig,

        "oldbalanceDest": transaction.oldbalanceDest,

        "newbalanceDest": transaction.newbalanceDest,

        "isFlaggedFraud": transaction.isFlaggedFraud,

        "type_CASH_OUT": 0,

        "type_DEBIT": 0,

        "type_PAYMENT": 0,

        "type_TRANSFER": 0,
    }


    # -----------------------------------------------------
    # ONE HOT ENCODING
    # -----------------------------------------------------

    transaction_type = transaction.type.upper()

    type_column = f"type_{transaction_type}"

    if type_column in row:

        row[type_column] = 1


    # -----------------------------------------------------
    # DATAFRAME
    # -----------------------------------------------------

    input_df = pd.DataFrame(
        [row],
        columns=FEATURES
    )


    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    prediction = int(
        model.predict(input_df)[0]
    )


    # -----------------------------------------------------
    # PROBABILITY
    # -----------------------------------------------------

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(input_df)[0]

        classes = list(model.classes_)

        if 1 in classes:

            fraud_index = classes.index(1)

            fraud_probability = float(
                probabilities[fraud_index]
            )

        else:

            fraud_probability = 0.0

    else:

        fraud_probability = 1.0 if prediction == 1 else 0.0


    safe_probability = 1.0 - fraud_probability


    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    if prediction == 1:

        result = "FRAUD"

        risk = "HIGH"

    else:

        result = "SAFE"

        # Probability based risk
        if fraud_probability >= 0.50:

            risk = "HIGH"

        elif fraud_probability >= 0.20:

            risk = "MEDIUM"

        else:

            risk = "LOW"


    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {

        "success": True,

        "result": result,

        "prediction": prediction,

        "risk": risk,

        "fraud_probability": round(
            fraud_probability * 100,
            2
        ),

        "safe_probability": round(
            safe_probability * 100,
            2
        ),

    }