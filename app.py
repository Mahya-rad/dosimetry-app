
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
    try:
        df = pd.read_excel("dosimetry-app/Cleaned_data.xlsx")
        st.write("Data loaded successfully!")
        st.write("Available columns:", df.columns.tolist())
        st.write("Data shape:", df.shape)
        
        # Check if required columns exist
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
        
        # Check which columns are missing
        missing_features = [col for col in features if col not in df.columns]
        missing_targets = [col for col in targets if col not in df.columns]
        
        if missing_features:
            st.error(f"Missing feature columns: {missing_features}")
        if missing_targets:
            st.error(f"Missing target columns: {missing_targets}")
            
        # Use only available columns
        available_features = [col for col in features if col in df.columns]
        available_targets = [col for col in targets if col in df.columns]
        
        if not available_features or not available_targets:
            st.error("Not enough required columns found in the data!")
            return None, None
            
        df = df[available_features + available_targets].dropna()
        X = df[available_features]
        y = df[available_targets]
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

    # Identify categorical and numerical columns from available features
    cat = [col for col in ["Intensity", "Laser Type"] if col in available_features]
    num = [col for col in available_features if col not in cat]

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

    return model, preprocessor, available_features, available_targets

result = load_model_and_preprocessor()
if result is None:
    st.error("Failed to load model. Please check the data file.")
    st.stop()

model, preprocessor, available_features, available_targets = result

# === Streamlit UI ===
st.set_page_config(
    page_title="Laser Therapy Parameter Predictor",
    page_icon="🔬",
    layout="wide"
)

st.title("Laser Therapy Parameter Predictor")
st.markdown("Predict optimal laser therapy parameters for medical treatment")

st.sidebar.header(" Patient Information")

age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=60)
freq = st.sidebar.slider("Sessions per Week", 1, 5, 3)
depth = st.sidebar.number_input("Tissue Penetration Depth (cm)", 0.5, 5.0, 2.0)
radius = st.sidebar.number_input("Laser Radius (cm)", 0.1, 2.0, 0.8)

# Laser Therapy Power Mode Selection
st.sidebar.subheader("🔬 Laser Therapy Mode")
laser_mode = st.sidebar.radio(
    "Select Laser Mode:",
    ["High-power (Class IV / HILT)", "Low-power (PBM / LLLT)"],
    key="laser_mode_radio"
)

# Initialize session state for power
if "power_w" not in st.session_state:
    st.session_state.power_w = 0.5  # Default to high-power minimum

# Define power ranges based on mode
if laser_mode == "High-power (Class IV / HILT)":
    min_power, max_power, step = 0.5, 30.0, 0.1
    default_power = 0.5
else:  # Low-power mode
    min_power, max_power, step = 0.005, 0.5, 0.005
    default_power = 0.005

# Clamp stored value to current range
st.session_state.power_w = max(min_power, min(max_power, st.session_state.power_w))

# Reset to range minimum if mode changed
if st.session_state.power_w < min_power or st.session_state.power_w > max_power:
    st.session_state.power_w = default_power

# Power slider
power_w = st.sidebar.slider(
    "Power (W)",
    min_value=min_power,
    max_value=max_power,
    value=st.session_state.power_w,
    step=step,
    key="power_slider"
)

# Update session state
st.session_state.power_w = power_w

# Display power information
st.sidebar.write(f"**Selected Power:** {power_w:.3f} W")
if laser_mode == "Low-power (PBM / LLLT)":
    power_mw = power_w * 1000
    st.sidebar.write(f"**Milliwatt Equivalent:** {power_mw:.1f} mW")

# Status line
st.sidebar.caption(f"**Mode:** {laser_mode} | **Range:** {min_power}-{max_power} W")

# Convert power to mW for compatibility with existing model
power = power_w * 1000  # Convert W to mW

intensity = st.sidebar.selectbox("Intensity", ["Low-Level", "High-Level"])
laser_type = st.sidebar.selectbox("Laser Type", ["CW", "PW"])

if st.sidebar.button("Predict Treatment Parameters", type="primary"):
    try:
        # Create input dictionary with only available features
        patient_input = {}
        if "Age" in available_features:
            patient_input["Age"] = age
        if "Frequency (sessions/week)" in available_features:
            patient_input["Frequency (sessions/week)"] = freq
        if "Penetration Depth" in available_features:
            patient_input["Penetration Depth"] = depth
        if "Laser Radius (cm)" in available_features:
            patient_input["Laser Radius (cm)"] = radius
        if "Power (mW)" in available_features:
            patient_input["Power (mW)"] = power
        if "Intensity" in available_features:
            patient_input["Intensity"] = intensity
        if "Laser Type" in available_features:
            patient_input["Laser Type"] = laser_type

        df_input = pd.DataFrame([patient_input])
        input_processed = preprocessor.transform(df_input)
        prediction = model.predict(input_processed)[0]

        st.subheader("Predicted Parameters:")
        
        # Display predictions based on available targets
        cols = st.columns(len(available_targets))
        
        for i, target in enumerate(available_targets):
            with cols[i]:
                if "Exposure Time" in target:
                    st.metric(
                        label="⏱️ Exposure Time",
                        value=f"{prediction[i]:.2f} s",
                        help="Recommended exposure duration"
                    )
                elif "Relaxation Time" in target:
                    st.metric(
                        label="🔄 Relaxation Time", 
                        value=f"{prediction[i]:.2f} µs",
                        help="Time between pulses"
                    )
                elif "Energy" in target:
                    st.metric(
                        label="⚡ Energy",
                        value=f"{prediction[i]:.2f} J",
                        help="Total energy delivered"
                    )
                else:
                    st.metric(
                        label=target,
                        value=f"{prediction[i]:.2f}",
                        help=f"Predicted {target}"
                    )
        
        # Additional information
        st.info("💡 **Note**: These are predicted values based on machine learning models. Always consult with medical professionals for clinical decisions.")
        
    except Exception as e:
        st.error(f"❌ Error occurred during prediction: {str(e)}")
        st.info("Please check your input values and try again.")
