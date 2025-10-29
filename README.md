# POS System - Business Management System

A comprehensive Point of Sale (POS) system built with **FastAPI** and **MySQL** for managing business operations including sales, purchases, supplier/customer management, inventory tracking, and financial cash flow.

## 🚀 Features

- ✅ **User Authentication**: Secure login with JWT tokens and role-based access (Admin/Staff)
- ✅ **Dashboard**: Real-time analytics with interactive charts for sales, purchases, inventory, and cash flow
- ✅ **Supplier Management**: Complete CRUD operations for supplier information
- ✅ **Customer Management**: Complete CRUD operations for customer information
- ✅ **Item Management**: Manage inventory items with stock tracking
- ✅ **Purchase Management**: Record purchases with automatic inventory updates
- ✅ **Sales Management**: Record sales with automatic inventory deduction and stock validation
- ✅ **Cash Flow Management**: Track financial inflows and outflows
- ✅ **Inventory Ledger**: Automatic tracking of all stock movements
- ✅ **Reports**: Generate inventory ledger reports

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js
- **Authentication**: JWT with password hashing

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- MySQL root user (no password)

## 🔧 Installation

### 1. Clone or Navigate to the Project Directory
```bash
cd "POS System"
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Create MySQL Database
Open MySQL and run:
```sql
CREATE DATABASE pos_system;
```

Or use the setup script:
```bash
python setup_database.py
```

## 🚀 Running the Application

### Option 1: Using the Start Script (Windows)
```bash
start.bat
```

### Option 2: Using Python Directly
```bash
python main.py
```

### Option 3: Using Uvicorn
```bash
uvicorn main:app --reload
```

### Access the Application
- Open your browser and navigate to: `http://localhost:8000`
- Default login credentials:
  - **Username**: `admin`
  - **Password**: `admin123`
  - **Role**: `admin`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` - User login

### Suppliers
- `GET /api/suppliers` - Get all suppliers
- `POST /api/suppliers` - Create supplier
- `PUT /api/suppliers/{id}` - Update supplier
- `DELETE /api/suppliers/{id}` - Delete supplier

### Customers
- `GET /api/customers` - Get all customers
- `POST /api/customers` - Create customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Items
- `GET /api/items` - Get all items
- `POST /api/items` - Create item
- `PUT /api/items/{id}` - Update item
- `DELETE /api/items/{id}` - Delete item

### Purchases
- `GET /api/purchases` - Get all purchases
- `GET /api/purchases/{id}` - Get purchase details
- `POST /api/purchases` - Create purchase

### Sales
- `GET /api/sales` - Get all sales
- `GET /api/sales/{id}` - Get sale details
- `POST /api/sales` - Create sale

### Cash Flow
- `GET /api/cashflow` - Get all cash flow entries
- `POST /api/cashflow` - Create cash flow entry
- `PUT /api/cashflow/{id}` - Update cash flow entry
- `DELETE /api/cashflow/{id}` - Delete cash flow entry

### Reports
- `GET /api/reports/dashboard` - Get dashboard data
- `GET /api/reports/inventory` - Get inventory ledger

## 🗄️ Database Schema

The system uses the following main tables:
- `users` - User authentication
- `suppliers` - Supplier information
- `customers` - Customer information
- `items` - Item catalog
- `purchase_master` - Purchase transactions header
- `purchase_details` - Purchase transaction line items
- `sales_master` - Sales transactions header
- `sales_details` - Sales transaction line items
- `cash_flow` - Financial inflows/outflows
- `item_ledger` - Inventory movement tracking

## 📖 Usage Guide

### Initial Setup

1. **Login** with admin credentials
2. **Add Suppliers** - Go to Suppliers module and add your suppliers
3. **Add Customers** - Go to Customers module and add your customers
4. **Add Items** - Go to Items module and add your inventory items
5. **Record Purchases** - Create purchase orders to increase inventory
6. **Record Sales** - Create sales transactions to decrease inventory
7. **Track Cash Flow** - Add cash inflows and outflows
8. **View Reports** - Check dashboard and inventory ledger for insights

### Purchase Process

1. Navigate to Purchases module
2. Click "New Purchase"
3. Select date and supplier
4. Add items with quantities and rates
5. Save to automatically update inventory

### Sales Process

1. Navigate to Sales module
2. Click "New Sale"
3. Select date and customer
4. Add items with quantities and rates
5. System checks stock availability
6. Save to automatically update inventory

## ✨ Key Features

- **Automatic Inventory Management**: Stock levels update automatically on purchases and sales
- **Inventory Ledger**: Tracks all stock movements with timestamps and references
- **Dashboard Analytics**: Visual charts for quick business insights
- **Role-Based Access**: Admin and Staff roles with different permissions
- **Real-Time Updates**: All changes reflect immediately in the system
- **Stock Validation**: Prevents sales if insufficient stock
- **MySQL Integration**: Uses MySQL database for production-ready applications

## 🔐 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- SQL injection protection via SQLAlchemy ORM
- CORS support for frontend integration

## 📁 Project Structure

```
POS System/
├── main.py              # FastAPI application
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication utilities
├── index.html           # Frontend HTML
├── static/
│   ├── styles.css       # CSS styles
│   └── script.js        # JavaScript functionality
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── start.bat           # Windows start script
```

## 🐛 Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Check database credentials in `database.py`
- Verify database `pos_system` exists

### Port Already in Use
- Change port in `main.py` or run: `uvicorn main:app --port 8001`

### Import Errors
- Activate virtual environment
- Run `pip install -r requirements.txt`

## 🚀 Future Enhancements

- Barcode scanning for sales and purchase entry
- Advanced reporting (Profit & Loss, GST reports)
- Integration with external payment gateways
- Mobile version of the app
- Multi-warehouse support
- Email notifications
- Export to Excel/PDF
- Barcode/QR code generation

## 📝 License

This project is created for educational and business purposes.

## 💬 Support

For issues or questions, please contact the development team.

## 🎯 System Requirements Alignment

This implementation fully aligns with the SRS (Software Requirements Specification):
- ✅ Database design matching SUPP_INFO, CUST_INFO, ITEM_MASTER, etc.
- ✅ Master-detail structure for purchases and sales
- ✅ Inventory ledger with IN/OUT movements
- ✅ Cash flow management with type tracking
- ✅ Dashboard reporting with graphs
- ✅ Role-based access control
- ✅ Complete CRUD operations

---

**Built with ❤️ using FastAPI and MySQL**

