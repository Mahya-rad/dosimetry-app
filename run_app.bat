@echo off
echo ========================================
echo    Laser Therapy Parameter Predictor
echo ========================================
echo.
echo Installing/updating dependencies...
py -3 -m pip install streamlit pandas scikit-learn openpyxl pillow numpy --quiet
echo.
echo Checking for required files...
if not exist "Cleaned_data.xlsx" (
    echo ERROR: Cleaned_data.xlsx not found!
    echo Please ensure the data file is in the same directory as this script.
    pause
    exit /b 1
)
if not exist "knee_diagram.png" (
    echo ERROR: knee_diagram.png not found!
    echo Please ensure the knee diagram image is in the same directory as this script.
    pause
    exit /b 1
)
echo All required files found!
echo.
echo Starting Streamlit server...
echo.
echo The app will open in your default web browser.
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
py -3 -m streamlit run app.py --server.headless false --server.port 8501
pause
