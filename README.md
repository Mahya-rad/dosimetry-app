
# 🔬 Laser Therapy Dosimetry Predictor

This is a web-based machine learning app for predicting optimal laser therapy parameters for patients with knee osteoarthritis (OA).

## 🚀 What It Does

Given basic patient and device input:
- Age
- Sessions per week
- Tissue penetration depth
- Laser radius
- Power (mW)
- Intensity (Low/High)
- Laser Type (CW/PW)

The app predicts:
- **Exposure Time** (in seconds)
- **Relaxation Time** (in microseconds)
- **Energy Delivered** (in Joules)

## 🧠 How It Works

The model uses:
- A real dataset of previous treatments (`Rofaydeh-Updated.xlsx`)
- Preprocessing (scaling, encoding, imputation)
- Multi-output Random Forest Regressor

## 🛠 How to Use (for developers)

1. Clone the repo or upload your data file.
2. Install dependencies:
```bash
pip install streamlit pandas scikit-learn openpyxl
```
3. Run the app:
```bash
streamlit run app.py
```

## 🌐 Or Use It Online

If deployed on [Streamlit Cloud](https://streamlit.io/cloud), just open the shared link.

---

Made with ❤️ by Mahya for an MSc thesis on optimizing dosimetry in laser therapy using machine learning.
