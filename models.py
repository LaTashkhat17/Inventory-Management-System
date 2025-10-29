from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"

class MovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"

class CashFlowType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"

class Status(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.STAFF)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    status = Column(SQLEnum(Status), default=Status.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    purchases = relationship("PurchaseMaster", back_populates="supplier")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    status = Column(SQLEnum(Status), default=Status.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales = relationship("SalesMaster", back_populates="customer")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    unit_of_measure = Column(String(20))
    current_stock = Column(Float, default=0.0)
    image = Column(String(255))  # Store image path instead of BLOB
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    purchase_details = relationship("PurchaseDetail", back_populates="item")
    sales_details = relationship("SalesDetail", back_populates="item")
    ledger_entries = relationship("ItemLedger", back_populates="item")

class PurchaseMaster(Base):
    __tablename__ = "purchase_master"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    purchase_date = Column(Date, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    total_amount = Column(Float, default=0.0)
    created_by = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="purchases")
    details = relationship("PurchaseDetail", back_populates="purchase", cascade="all, delete-orphan")

class PurchaseDetail(Base):
    __tablename__ = "purchase_details"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    purchase_id = Column(Integer, ForeignKey("purchase_master.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    
    # Relationships
    purchase = relationship("PurchaseMaster", back_populates="details")
    item = relationship("Item", back_populates="purchase_details")

class SalesMaster(Base):
    __tablename__ = "sales_master"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sales_date = Column(Date, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Float, default=0.0)
    created_by = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="sales")
    details = relationship("SalesDetail", back_populates="sales", cascade="all, delete-orphan")

class SalesDetail(Base):
    __tablename__ = "sales_details"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sales_id = Column(Integer, ForeignKey("sales_master.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    
    # Relationships
    sales = relationship("SalesMaster", back_populates="details")
    item = relationship("Item", back_populates="sales_details")

class CashFlow(Base):
    __tablename__ = "cash_flow"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_date = Column(Date, nullable=False)
    type = Column(SQLEnum(CashFlowType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    ref_id = Column(String(50))  # Reference to purchase/sales ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ItemLedger(Base):
    __tablename__ = "item_ledger"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    movement_date = Column(Date, nullable=False)
    movement_type = Column(SQLEnum(MovementType), nullable=False)
    quantity = Column(Float, nullable=False)
    movement_reference = Column(String(100))  # Reference to purchase/sales
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    item = relationship("Item", back_populates="ledger_entries")

