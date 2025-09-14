
# Laser Therapy Parameter Predictor

A web-based machine learning application for predicting optimal laser therapy parameters for medical treatment, specifically designed for knee therapy applications.

## 🎯 What It Does

The app uses machine learning to predict optimal laser therapy parameters based on:
- **Patient Information**: Age, treatment frequency
- **Treatment Parameters**: Penetration depth, laser radius
- **Laser Configuration**: Power level, intensity, laser type (CW/PW)
- **Treatment Points**: Interactive selection of knee anatomy points

**Predictions Include:**
- ⏱️ **Exposure Time** (seconds)
- 🔄 **Relaxation Time** (microseconds) 
- ⚡ **Total Energy** (Joules)
- 📊 **Dose per Treatment Point** (calculated distribution)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Required files: `Cleaned_data.xlsx` and `knee_diagram.png`

### Installation & Running

#### Option 1: Using requirements.txt (Recommended)
```bash
# Clone or download the repository
git clone <repository-url>
cd dosimetry-app

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

#### Option 2: Manual Installation
```bash
# Install required packages
pip install streamlit pandas scikit-learn openpyxl pillow numpy

# Run the application
streamlit run app.py
```

### Platform-Specific Launchers

#### Windows
```bash
# Double-click run_app.bat or run in Command Prompt
run_app.bat
```

#### macOS/Linux
```bash
# Make executable and run
chmod +x run_app.sh
./run_app.sh
```

#### PowerShell (Windows)
```powershell
# Run the PowerShell script
.\run_app.ps1
```

## 📁 Required Files

Ensure these files are in the same directory as `app.py`:
- `Cleaned_data.xlsx` - Training data for the ML model
- `knee_diagram.png` - Interactive knee anatomy diagram

## 🌐 Online Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click

### Other Platforms
- **Heroku**: Use the included `Procfile`
- **Docker**: Use the included `Dockerfile`
- **Local Network**: Access via `http://localhost:8501`

## 🛠️ Technical Details

### Machine Learning Model
- **Algorithm**: Multi-output Random Forest Regressor
- **Preprocessing**: StandardScaler, OneHotEncoder, SimpleImputer
- **Features**: 7 input parameters
- **Targets**: 3 output predictions

### Dependencies
- `streamlit>=1.28.0` - Web framework
- `pandas>=1.5.0` - Data manipulation
- `scikit-learn>=1.3.0` - Machine learning
- `openpyxl>=3.1.0` - Excel file support
- `pillow>=9.0.0` - Image processing
- `numpy>=1.24.0` - Numerical computing

## 📖 How to Use

1. **Select Treatment Points**: Use the interactive buttons to select knee anatomy points
2. **Configure Parameters**: Set patient information and laser settings in the sidebar
3. **Predict Parameters**: Click "Predict Treatment Parameters" to get recommendations
4. **Review Results**: View predicted parameters and dose distribution per point

## ⚠️ Important Notes

- **Medical Disclaimer**: This tool is for research and educational purposes only
- **Professional Consultation**: Always consult qualified medical professionals for clinical decisions
- **Data Privacy**: No patient data is stored or transmitted

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of an MSc thesis research. Please cite appropriately if used in academic work.

## 👨‍💻 Author

Made with ❤️ by **Mahya** for MSc thesis research on optimizing dosimetry in laser therapy using machine learning.

---

**Need Help?** Open an issue on GitHub or contact the author.
