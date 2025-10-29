from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime
from models import UserRole, Status, MovementType, CashFlowType

# Authentication Schemas
class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

# Supplier Schemas
class SupplierBase(BaseModel):
    name: str
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    status: Status = Status.ACTIVE

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    status: Optional[Status] = None

class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    status: Status = Status.ACTIVE

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    status: Optional[Status] = None

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Item Schemas
class ItemBase(BaseModel):
    name: str
    unit_of_measure: Optional[str] = None
    current_stock: float = 0.0

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    unit_of_measure: Optional[str] = None
    current_stock: Optional[float] = None

class ItemResponse(ItemBase):
    id: int
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Purchase Schemas
class PurchaseDetailBase(BaseModel):
    item_id: int
    quantity: float
    rate: float

class PurchaseDetailResponse(PurchaseDetailBase):
    id: int
    purchase_id: int
    
    class Config:
        from_attributes = True

class PurchaseMasterBase(BaseModel):
    purchase_date: date
    supplier_id: int
    details: List[PurchaseDetailBase]

class PurchaseCreate(PurchaseMasterBase):
    pass

class PurchaseMasterResponse(BaseModel):
    id: int
    purchase_date: date
    supplier_id: int
    total_amount: float
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PurchaseMasterDetailResponse(BaseModel):
    master: PurchaseMasterResponse
    details: List[PurchaseDetailResponse]

# Sales Schemas
class SalesDetailBase(BaseModel):
    item_id: int
    quantity: float
    rate: float

class SalesDetailResponse(SalesDetailBase):
    id: int
    sales_id: int
    
    class Config:
        from_attributes = True

class SalesMasterBase(BaseModel):
    sales_date: date
    customer_id: int
    details: List[SalesDetailBase]

class SalesCreate(SalesMasterBase):
    pass

class SalesMasterResponse(BaseModel):
    id: int
    sales_date: date
    customer_id: int
    total_amount: float
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SalesMasterDetailResponse(BaseModel):
    master: SalesMasterResponse
    details: List[SalesDetailResponse]

# Cash Flow Schemas
class CashFlowBase(BaseModel):
    transaction_date: date
    type: CashFlowType
    amount: float
    description: Optional[str] = None
    ref_id: Optional[str] = None

class CashFlowCreate(CashFlowBase):
    pass

class CashFlowUpdate(BaseModel):
    transaction_date: Optional[date] = None
    type: Optional[CashFlowType] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    ref_id: Optional[str] = None

class CashFlowResponse(CashFlowBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Item Ledger Schemas
class ItemLedgerResponse(BaseModel):
    id: int
    item_id: int
    movement_date: date
    movement_type: MovementType
    quantity: float
    movement_reference: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardResponse(BaseModel):
    total_sales: float
    total_purchases: float
    net_cashflow: float
    total_items: int
    sales_data: List[dict]
    purchase_data: List[dict]
    cashflow_data: List[dict]

