#!/bin/bash

echo "========================================"
echo "   Laser Therapy Parameter Predictor"
echo "========================================"
echo ""
echo "Installing/updating dependencies..."
pip3 install -r requirements.txt --quiet
echo ""
echo "Checking for required files..."
if [ ! -f "Cleaned_data.xlsx" ]; then
    echo "ERROR: Cleaned_data.xlsx not found!"
    echo "Please ensure the data file is in the same directory as this script."
    exit 1
fi
if [ ! -f "knee_diagram.png" ]; then
    echo "ERROR: knee_diagram.png not found!"
    echo "Please ensure the knee diagram image is in the same directory as this script."
    exit 1
fi
echo "All required files found!"
echo ""
echo "Starting Streamlit server..."
echo ""
echo "The app will open in your default web browser."
echo "If it doesn't open automatically, go to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
streamlit run app.py --server.headless false --server.port 8501
