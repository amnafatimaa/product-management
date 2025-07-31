from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: float
    category: str
    description: Optional[str] = None

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    data: List[ProductResponse]
    total: int
    page: int
    limit: int
    total_pages: int
class BulkUploadRequest(BaseModel):
    products: List[ProductCreate]