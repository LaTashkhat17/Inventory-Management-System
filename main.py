from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List, Optional
from pathlib import Path

from database import SessionLocal, engine, Base, get_db
from models import (
    User, Supplier, Customer, Item, PurchaseMaster, PurchaseDetail,
    SalesMaster, SalesDetail, CashFlow, ItemLedger, UserRole, Status,
    MovementType, CashFlowType
)
from schemas import *
from auth import verify_token, get_password_hash, create_access_token, verify_password

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="POS System API",
    description="Business Management System - Point of Sale with Inventory Tracking",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Security
security = HTTPBearer()

# Dependency to get current user
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(User).filter(User.username == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

# Initialize default admin user
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role=UserRole.ADMIN
            )
            db.add(admin)
            db.commit()
            print("Default admin user created")
    finally:
        db.close()

# ============================================
# AUTHENTICATION ENDPOINTS
# ============================================

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if user.role.value != credentials.role:
        raise HTTPException(status_code=403, detail="Invalid role")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role.value}

# ============================================
# SUPPLIER ENDPOINTS
# ============================================

@app.get("/api/suppliers", response_model=List[SupplierResponse])
def get_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    suppliers = db.query(Supplier).offset(skip).limit(limit).all()
    return suppliers

@app.post("/api/suppliers", response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@app.put("/api/suppliers/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    for key, value in supplier.dict(exclude_unset=True).items():
        setattr(db_supplier, key, value)
    
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@app.delete("/api/suppliers/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    db.delete(db_supplier)
    db.commit()
    return {"message": "Supplier deleted successfully"}

# ============================================
# CUSTOMER ENDPOINTS
# ============================================

@app.get("/api/customers", response_model=List[CustomerResponse])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@app.post("/api/customers", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.put("/api/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.delete("/api/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    return {"message": "Customer deleted successfully"}

# ============================================
# ITEM ENDPOINTS
# ============================================

@app.get("/api/items", response_model=List[ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

@app.post("/api/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/api/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}

# ============================================
# PURCHASE ENDPOINTS
# ============================================

@app.get("/api/purchases", response_model=List[PurchaseMasterResponse])
def get_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    purchases = db.query(PurchaseMaster).offset(skip).limit(limit).all()
    return purchases

@app.get("/api/purchases/{purchase_id}", response_model=PurchaseMasterDetailResponse)
def get_purchase(purchase_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    purchase = db.query(PurchaseMaster).filter(PurchaseMaster.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    details = db.query(PurchaseDetail).filter(PurchaseDetail.purchase_id == purchase_id).all()
    return {"master": purchase, "details": details}

@app.post("/api/purchases", response_model=PurchaseMasterResponse)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Create purchase master
    try:
        db_purchase = PurchaseMaster(
            purchase_date=purchase.purchase_date,
            supplier_id=purchase.supplier_id,
            created_by=current_user.username
        )
        db.add(db_purchase)
        db.flush()
        
        # Create purchase details and update inventory
        total_amount = 0.0
        for detail in purchase.details:
            db_detail = PurchaseDetail(
                purchase_id=db_purchase.id,
                item_id=detail.item_id,
                quantity=detail.quantity,
                rate=detail.rate
            )
            db.add(db_detail)
            total_amount += detail.quantity * detail.rate
            
            # Update item stock
            item = db.query(Item).filter(Item.id == detail.item_id).first()
            if item:
                item.current_stock += detail.quantity
            
            # Create ledger entry
            ledger = ItemLedger(
                item_id=detail.item_id,
                movement_date=purchase.purchase_date,
                movement_type=MovementType.IN,
                quantity=detail.quantity,
                movement_reference=f"PURCHASE-{db_purchase.id}"
            )
            db.add(ledger)
        
        db_purchase.total_amount = total_amount
        
        # Create cash flow entry for purchase (OUTFLOW)
        cashflow = CashFlow(
            transaction_date=purchase.purchase_date,
            type=CashFlowType.OUT,
            amount=total_amount,
            description=f"Purchase from Supplier - Purchase #{db_purchase.id}",
            ref_id=f"PURCHASE-{db_purchase.id}"
        )
        db.add(cashflow)
        
        # Commit everything together
        db.commit()
        db.refresh(db_purchase)
        
        print(f"✅ Purchase created: ID={db_purchase.id}, Amount={total_amount}, CashFlow added")
        return db_purchase
            
    except HTTPException:
        db.rollback()
        print("❌ Purchase failed: HTTPException")
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Purchase failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create purchase: {str(e)}")

# ============================================
# SALES ENDPOINTS
# ============================================

@app.get("/api/sales", response_model=List[SalesMasterResponse])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sales = db.query(SalesMaster).offset(skip).limit(limit).all()
    return sales

@app.get("/api/sales/{sales_id}", response_model=SalesMasterDetailResponse)
def get_sale(sales_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sale = db.query(SalesMaster).filter(SalesMaster.id == sales_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    details = db.query(SalesDetail).filter(SalesDetail.sales_id == sales_id).all()
    return {"master": sale, "details": details}

@app.post("/api/sales", response_model=SalesMasterResponse)
def create_sale(sale: SalesCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Create sales master
    try:
        db_sale = SalesMaster(
            sales_date=sale.sales_date,
            customer_id=sale.customer_id,
            created_by=current_user.username
        )
        db.add(db_sale)
        db.flush()
        
        # Create sales details and update inventory
        total_amount = 0.0
        for detail in sale.details:
            # Check stock availability
            item = db.query(Item).filter(Item.id == detail.item_id).first()
            if not item:
                raise HTTPException(status_code=404, detail=f"Item {detail.item_id} not found")
            if item.current_stock < detail.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for item {item.name}. Available: {item.current_stock}")
            
            db_detail = SalesDetail(
                sales_id=db_sale.id,
                item_id=detail.item_id,
                quantity=detail.quantity,
                rate=detail.rate
            )
            db.add(db_detail)
            total_amount += detail.quantity * detail.rate
            
            # Update item stock
            item.current_stock -= detail.quantity
            
            # Create ledger entry
            ledger = ItemLedger(
                item_id=detail.item_id,
                movement_date=sale.sales_date,
                movement_type=MovementType.OUT,
                quantity=detail.quantity,
                movement_reference=f"SALES-{db_sale.id}"
            )
            db.add(ledger)
        
        db_sale.total_amount = total_amount
        
        # Create cash flow entry for sales (INFLOW)
        cashflow = CashFlow(
                transaction_date=sale.sales_date,
                type=CashFlowType.IN,
                amount=total_amount,
                description=f"Sale to Customer - Sales #{db_sale.id}",
                ref_id=f"SALES-{db_sale.id}"
            )
        db.add(cashflow)
        
        # Commit everything together
        db.commit()
        db.refresh(db_sale)
        
        print(f"✅ Sale created: ID={db_sale.id}, Amount={total_amount}, CashFlow added")
        return db_sale
        
    except HTTPException:
        db.rollback()
        print("❌ Sale failed: HTTPException")
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Sale failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create sale: {str(e)}")

# ============================================
# CASH FLOW ENDPOINTS
# ============================================

@app.get("/api/cashflow", response_model=List[CashFlowResponse])
def get_cashflow(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cashflows = db.query(CashFlow).offset(skip).limit(limit).all()
    return cashflows

@app.post("/api/cashflow", response_model=CashFlowResponse)
def create_cashflow(cashflow: CashFlowCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_cashflow = CashFlow(**cashflow.dict())
    db.add(db_cashflow)
    db.commit()
    db.refresh(db_cashflow)
    return db_cashflow

@app.put("/api/cashflow/{cashflow_id}", response_model=CashFlowResponse)
def update_cashflow(cashflow_id: int, cashflow: CashFlowUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_cashflow = db.query(CashFlow).filter(CashFlow.id == cashflow_id).first()
    if not db_cashflow:
        raise HTTPException(status_code=404, detail="Cash flow entry not found")
    
    for key, value in cashflow.dict(exclude_unset=True).items():
        setattr(db_cashflow, key, value)
    
    db.commit()
    db.refresh(db_cashflow)
    return db_cashflow

@app.delete("/api/cashflow/{cashflow_id}")
def delete_cashflow(cashflow_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_cashflow = db.query(CashFlow).filter(CashFlow.id == cashflow_id).first()
    if not db_cashflow:
        raise HTTPException(status_code=404, detail="Cash flow entry not found")
    
    db.delete(db_cashflow)
    db.commit()
    return {"message": "Cash flow entry deleted successfully"}

# ============================================
# REPORTS ENDPOINTS
# ============================================

@app.get("/api/reports/inventory", response_model=List[ItemLedgerResponse])
def get_inventory_report(item_id: Optional[int] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(ItemLedger)
    if item_id:
        query = query.filter(ItemLedger.item_id == item_id)
    
    ledger_entries = query.order_by(ItemLedger.movement_date.desc()).all()
    return ledger_entries

@app.get("/api/reports/dashboard", response_model=DashboardResponse)
def get_dashboard_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Calculate totals
    total_sales = db.query(func.sum(SalesMaster.total_amount)).scalar() or 0.0
    total_purchases = db.query(func.sum(PurchaseMaster.total_amount)).scalar() or 0.0
    
    # Cash flow totals
    total_inflow = db.query(func.sum(CashFlow.amount)).filter(CashFlow.type == CashFlowType.IN).scalar() or 0.0
    total_outflow = db.query(func.sum(CashFlow.amount)).filter(CashFlow.type == CashFlowType.OUT).scalar() or 0.0
    net_cashflow = total_inflow - total_outflow
    
    # Total items
    total_items = db.query(func.count(Item.id)).scalar() or 0
    
    # Recent transactions for charts
    sales_data = db.query(SalesMaster).order_by(SalesMaster.sales_date.desc()).limit(10).all()
    purchase_data = db.query(PurchaseMaster).order_by(PurchaseMaster.purchase_date.desc()).limit(10).all()
    cashflow_data = db.query(CashFlow).order_by(CashFlow.transaction_date.desc()).limit(10).all()
    
    return {
        "total_sales": float(total_sales),
        "total_purchases": float(total_purchases),
        "net_cashflow": float(net_cashflow),
        "total_items": total_items,
        "sales_data": [{"date": str(s.sales_date), "amount": float(s.total_amount)} for s in sales_data],
        "purchase_data": [{"date": str(p.purchase_date), "amount": float(p.total_amount)} for p in purchase_data],
        "cashflow_data": [{"date": str(c.transaction_date), "type": c.type.value, "amount": float(c.amount)} for c in cashflow_data]
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("Starting POS System - Business Management")
    print("="*50)
    print("\nDatabase: MySQL")
    print("API: FastAPI")
    print("Server: http://localhost:8000")
    print("Admin Login: admin / admin123")
    print("\n" + "="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

