@echo off
echo Starting Loan Approval Prediction System...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting the application...
echo The system will be available at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
