from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="Identity Theft Detection API",
    description="Machine Learning API for fraudulent transaction detection",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================
# Frontend localhost:5173 / 5175 etc. se connect ho sake
# Is project mein authentication/cookies use nahi ho rahe,
# isliye allow_credentials=False rakha gaya hai.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# MODEL FILE PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "identity_theft_random_forest.pkl"
SCALER_PATH = BASE_DIR / "identity_theft_scaler.pkl"


# =========================================================
# LOAD MODEL + SCALER
# =========================================================

model = None
scaler = None


try:

    print("\n==============================")
    print("Loading ML Model...")
    print("==============================")

    model = joblib.load(MODEL_PATH)

    print("✅ Random Forest model loaded")
    print("Model:", type(model).__name__)

    scaler = joblib.load(SCALER_PATH)

    print("✅ Scaler loaded")
    print("Scaler:", type(scaler).__name__)

    # Show model/scaler features if available
    if hasattr(scaler, "feature_names_in_"):

        print("\nScaler expected features:")

        for feature in scaler.feature_names_in_:
            print("  -", feature)

    elif hasattr(model, "feature_names_in_"):

        print("\nModel expected features:")

        for feature in model.feature_names_in_:
            print("  -", feature)

    print("==============================\n")


except Exception as e:

    print("\n❌ MODEL LOADING ERROR")
    print(e)
    print("==============================\n")


# =========================================================
# REQUEST MODEL
# =========================================================

class Transaction(BaseModel):

    step: float

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
        "message": "Identity Theft Detection API is running",
        "model": "Random Forest",
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
    }


# =========================================================
# CREATE ALL POSSIBLE FEATURES
# =========================================================

def create_features(transaction: Transaction):

    data = {

        # Numeric features
        "step": transaction.step,

        "amount": transaction.amount,

        "oldbalanceOrg": transaction.oldbalanceOrg,

        "newbalanceOrig": transaction.newbalanceOrig,

        "oldbalanceDest": transaction.oldbalanceDest,

        "newbalanceDest": transaction.newbalanceDest,

        "isFlaggedFraud": transaction.isFlaggedFraud,

        # Normal names
        "CASH_IN": 0,
        "CASH_OUT": 0,
        "DEBIT": 0,
        "PAYMENT": 0,
        "TRANSFER": 0,

        # sklearn/pandas one-hot names
        "type_CASH_IN": 0,
        "type_CASH_OUT": 0,
        "type_DEBIT": 0,
        "type_PAYMENT": 0,
        "type_TRANSFER": 0,
    }


    transaction_type = transaction.type.upper().strip()


    # Normal feature name
    if transaction_type in [
        "CASH_IN",
        "CASH_OUT",
        "DEBIT",
        "PAYMENT",
        "TRANSFER",
    ]:

        data[transaction_type] = 1


    # type_ feature name
    type_feature = f"type_{transaction_type}"

    if type_feature in data:

        data[type_feature] = 1


    return data


# =========================================================
# GET EXPECTED FEATURES
# =========================================================

def get_expected_features():

    # Prefer scaler feature names
    if hasattr(scaler, "feature_names_in_"):

        return list(scaler.feature_names_in_)


    # Otherwise use model feature names
    if hasattr(model, "feature_names_in_"):

        return list(model.feature_names_in_)


    # Fallback
    return [
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
# PREDICT
# =========================================================

@app.post("/predict")
def predict(transaction: Transaction):

    # -----------------------------------------------------
    # Check model
    # -----------------------------------------------------

    if model is None:

        raise HTTPException(
            status_code=500,
            detail="Random Forest model is not loaded.",
        )


    if scaler is None:

        raise HTTPException(
            status_code=500,
            detail="Scaler is not loaded.",
        )


    try:

        # -------------------------------------------------
        # CREATE FEATURES
        # -------------------------------------------------

        features = create_features(transaction)


        print("\n==============================")
        print("NEW TRANSACTION")
        print("==============================")

        print(transaction.model_dump())


        # -------------------------------------------------
        # CREATE DATAFRAME
        # -------------------------------------------------

        df = pd.DataFrame([features])


        # -------------------------------------------------
        # GET EXACT MODEL FEATURES
        # -------------------------------------------------

        expected_features = get_expected_features()


        print("\nExpected model features:")

        print(expected_features)


        # -------------------------------------------------
        # ADD MISSING FEATURES
        # -------------------------------------------------

        for feature in expected_features:

            if feature not in df.columns:

                df[feature] = 0


        # -------------------------------------------------
        # REMOVE EXTRA FEATURES
        # AND KEEP EXACT ORDER
        # -------------------------------------------------

        df = df[expected_features]


        print("\nFinal features sent to model:")

        print(df)


        # -------------------------------------------------
        # SCALE
        # -------------------------------------------------

        features_scaled = scaler.transform(df)


        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        prediction = int(
            model.predict(features_scaled)[0]
        )


        # -------------------------------------------------
        # PROBABILITY
        # -------------------------------------------------

        probability = model.predict_proba(
            features_scaled
        )[0]


        # -------------------------------------------------
        # SAFE / FRAUD PROBABILITY
        # -------------------------------------------------

        # Find class indexes safely
        classes = list(model.classes_)


        if 0 in classes:

            safe_index = classes.index(0)

            safe_probability = float(
                probability[safe_index] * 100
            )

        else:

            safe_probability = 0.0


        if 1 in classes:

            fraud_index = classes.index(1)

            fraud_probability = float(
                probability[fraud_index] * 100
            )

        else:

            fraud_probability = 0.0


        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        if prediction == 1:

            result = "FRAUD"

            risk = "HIGH"

        else:

            result = "SAFE"

            risk = "LOW"


        # -------------------------------------------------
        # FINAL RESPONSE
        # -------------------------------------------------

        response = {

            "prediction": prediction,

            "result": result,

            "risk": risk,

            "fraud_probability": round(
                fraud_probability,
                2,
            ),

            "safe_probability": round(
                safe_probability,
                2,
            ),
        }


        print("\n==============================")
        print("PREDICTION RESULT")
        print("==============================")

        print(response)

        print("==============================\n")


        return response


    except Exception as e:

        print("\n==============================")
        print("❌ PREDICTION ERROR")
        print("==============================")

        print(type(e).__name__)
        print(str(e))

        print("==============================\n")


        raise HTTPException(
            status_code=500,
            detail=str(e),
        )