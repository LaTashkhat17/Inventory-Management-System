@echo off
echo ========================================
echo   POS System - Business Management
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check MySQL connection
echo.
echo Checking MySQL connection...
python -c "import pymysql; pymysql.connect(host='localhost', user='root', password='')" 2>nul
if errorlevel 1 (
    echo ERROR: Cannot connect to MySQL
    echo Please ensure MySQL is running and accessible
    pause
    exit /b 1
)

REM Create database if needed
echo.
echo Setting up database...
python setup_database.py

REM Start the server
echo.
echo ========================================
echo   Starting FastAPI server...
echo ========================================
echo.
echo Server will be available at: http://localhost:8000
echo Default login: admin / admin123
echo.
echo ========================================
echo.

python main.py

pause
