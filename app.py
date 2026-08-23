from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import joblib


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="Identity Guard API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    # Exact allowed origins
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5175",

        # Vercel production
        "https://identity-theft-detection.vercel.app",
    ],

    # Allow Vercel preview deployment URLs
    allow_origin_regex=r"https://.*\.vercel\.app",

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

    print("========================================")
    print("✅ Random Forest model loaded successfully")
    print("========================================")

except Exception as e:

    print("========================================")
    print("❌ Model loading failed")
    print("Error:", e)
    print("========================================")


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
        "message": "Identity Guard API is running",
        "version": "1.0.0"
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

    # -----------------------------------------------------
    # CHECK MODEL
    # -----------------------------------------------------

    if model is None:

        return {
            "success": False,
            "error": "Random Forest model could not be loaded."
        }


    # -----------------------------------------------------
    # CREATE INPUT ROW
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

    transaction_type = transaction.type.upper().strip()

    type_column = f"type_{transaction_type}"

    if type_column in row:

        row[type_column] = 1


    # -----------------------------------------------------
    # CREATE DATAFRAME
    # -----------------------------------------------------

    input_df = pd.DataFrame(
        [row],
        columns=FEATURES
    )


    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    try:

        prediction = int(
            model.predict(input_df)[0]
        )

    except Exception as e:

        return {
            "success": False,
            "error": f"Prediction failed: {str(e)}"
        }


    # -----------------------------------------------------
    # FRAUD PROBABILITY
    # -----------------------------------------------------

    if hasattr(model, "predict_proba"):

        try:

            probabilities = model.predict_proba(
                input_df
            )[0]

            classes = list(model.classes_)

            if 1 in classes:

                fraud_index = classes.index(1)

                fraud_probability = float(
                    probabilities[fraud_index]
                )

            else:

                fraud_probability = 0.0

        except Exception:

            fraud_probability = (
                1.0 if prediction == 1 else 0.0
            )

    else:

        fraud_probability = (
            1.0 if prediction == 1 else 0.0
        )


    # -----------------------------------------------------
    # SAFE PROBABILITY
    # -----------------------------------------------------

    safe_probability = 1.0 - fraud_probability


    # -----------------------------------------------------
    # RESULT + RISK
    # -----------------------------------------------------

    if prediction == 1:

        result = "FRAUD"

        risk = "HIGH"

    else:

        result = "SAFE"

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