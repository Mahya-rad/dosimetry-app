
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# === Load Data and Train Model ===
@st.cache_resource
def load_model_and_preprocessor():
    df = pd.read_excel("Rofaydeh-Updated.xlsx")

    features = [
        "Age", 
        "Frequency (sessions/week)", 
        "Penetration Depth", 
        "Laser Radius (cm)", 
        "Power (mW)", 
        "Intensity", 
        "Laser Type"
    ]
    targets = [
        "Exposure Time (s)", 
        "Relaxation Time (µs)", 
        "Energy (J)"
    ]

    df = df[features + targets].dropna()
    X = df[features]
    y = df[targets]

    cat = ["Intensity", "Laser Type"]
    num = list(set(features) - set(cat))

    preprocessor = ColumnTransformer([
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler())
        ]), num),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(drop="first"))
        ]), cat)
    ])

    X_processed = preprocessor.fit_transform(X)
    model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
    model.fit(X_processed, y)

    return model, preprocessor

model, preprocessor = load_model_and_preprocessor()

# === Streamlit UI ===
st.title("🔬 Laser Therapy Parameter Predictor")

st.sidebar.header("Patient Information")

age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=60)
freq = st.sidebar.slider("Sessions per Week", 1, 5, 3)
depth = st.sidebar.number_input("Tissue Penetration Depth (cm)", 0.5, 5.0, 2.0)
radius = st.sidebar.number_input("Laser Radius (cm)", 0.1, 2.0, 0.8)
power = st.sidebar.number_input("Power (mW)", 100, 1000, 400)
intensity = st.sidebar.selectbox("Intensity", ["Low-Level", "High-Level"])
laser_type = st.sidebar.selectbox("Laser Type", ["CW", "PW"])

if st.sidebar.button("Predict Treatment Parameters"):
    patient_input = {
        "Age": age,
        "Frequency (sessions/week)": freq,
        "Penetration Depth": depth,
        "Laser Radius (cm)": radius,
        "Power (mW)": power,
        "Intensity": intensity,
        "Laser Type": laser_type
    }

    df_input = pd.DataFrame([patient_input])
    input_processed = preprocessor.transform(df_input)
    prediction = model.predict(input_processed)[0]

    st.subheader("📊 Predicted Parameters:")
    st.success(f"• Exposure Time: {prediction[0]:.2f} seconds")
    st.success(f"• Relaxation Time: {prediction[1]:.2f} µs")
    st.success(f"• Energy: {prediction[2]:.2f} J")
