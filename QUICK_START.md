# Quick Start Guide - POS System

## Prerequisites
- Python 3.8+
- MySQL Server (root user, no password)
- MySQL must be running

## Installation & Setup

### Step 1: Double-click `start.bat`
The script will:
- Install all dependencies
- Create the database
- Start the server

### Step 2: Open Browser
Navigate to: **http://localhost:8000**

### Step 3: Login
- Username: `admin`
- Password: `admin123`
- Role: `admin`

## Manual Setup (Alternative)

If you prefer manual setup:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create database
python setup_database.py

# 3. Start server
python main.py
```

## Troubleshooting

### MySQL Connection Error
- Make sure MySQL Server is running
- Check MySQL credentials in `database.py`

### Port Already in Use
- Stop any process using port 8000
- Or change port in `main.py`

### Import Errors
- Run: `pip install -r requirements.txt`
- Restart the server

## Features

✅ **Dashboard** - Real-time analytics with charts
✅ **Suppliers** - Manage supplier information
✅ **Customers** - Manage customer information  
✅ **Items** - Track inventory items
✅ **Purchases** - Record purchases (auto-updates inventory & cash flow)
✅ **Sales** - Record sales (auto-updates inventory & cash flow)
✅ **Cash Flow** - View automatic cash flow entries
✅ **Reports** - Generate inventory ledger reports

## System Status

The server is running when you see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Need Help?

Check the full README.md for detailed documentation.

