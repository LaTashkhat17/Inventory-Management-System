# How to Run the POS System

## ✅ Your Server is Already Running!

Based on the logs, your server is successfully running on port 8000.

### Access the System:
1. Open your browser
2. Go to: **http://localhost:8000**
3. Login with:
   - Username: `admin`
   - Password: `admin123`
   - Role: `admin`

## Starting the Server

### Method 1: Double-click (Recommended)
**Double-click `start.bat`** in Windows Explorer

### Method 2: Command Line
Open Command Prompt in the project folder and run:
```bash
start.bat
```

### Method 3: Direct Python
```bash
python main.py
```

## Stopping the Server

Press **Ctrl + C** in the terminal where the server is running

## If Port 8000 is Busy

### Option 1: Stop the existing server
Find the running process and stop it

### Option 2: Use a different port
Edit `main.py` line 440 and change port:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed to 8001
```

## System Features Working

✅ **Dashboard** - Analytics and charts
✅ **Suppliers** - CRUD operations
✅ **Customers** - CRUD operations
✅ **Items** - Inventory management
✅ **Purchases** - Auto-updates inventory & cash flow
✅ **Sales** - Auto-updates inventory & cash flow
✅ **Cash Flow** - Automatic tracking
✅ **Reports** - Inventory ledger

## Current Status

Your system is **ready to use**. The server logs show successful operations:
- User login working
- Data retrieval working
- CRUD operations working
- Cash flow auto-updating from purchases/sales

Just open http://localhost:8000 in your browser!

