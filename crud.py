from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import Product
from schemas import ProductCreate, ProductUpdate
from typing import Optional

def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "id",
    order: str = "asc"
):
    query = db.query(Product)
    
    # Apply filters
    filters = []
    
    if search:
        filters.append(
            or_(
                Product.name.contains(search),
                Product.description.contains(search)
            )
        )
    
    if category:
        filters.append(Product.category == category)
    
    if min_price is not None:
        filters.append(Product.price >= min_price)
    
    if max_price is not None:
        filters.append(Product.price <= max_price)
    
    if filters:
        query = query.filter(and_(*filters))
    
    # Apply sorting
    sort_column = getattr(Product, sort_by, Product.id)
    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    products = query.offset(skip).limit(limit).all()
    
    return products, total

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        update_data = product.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

def get_categories(db: Session):
    return db.query(Product.category).distinct().all()