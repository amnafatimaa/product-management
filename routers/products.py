from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import crud
import schemas
from database import get_db
import math

router = APIRouter()

@router.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@router.get("/products", response_model=schemas.PaginatedResponse)
def read_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    sort_by: str = Query("id", regex="^(id|name|price|category|created_at)$"),
    order: str = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    products, total = crud.get_products(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        order=order
    )
    
    total_pages = math.ceil(total / limit)
    
    return schemas.PaginatedResponse(
        data=products,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )

@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int, 
    product: schemas.ProductUpdate, 
    db: Session = Depends(get_db)
):
    db_product = crud.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return [cat[0] for cat in categories if cat[0]]

# routers/products.py (excerpt)
@router.post("/products/bulk-upload")
def bulk_upload_products(products: schemas.BulkUploadRequest, db: Session = Depends(get_db)):
    try:
        created_products = []
        for product in products.products:
            created_product = crud.create_product(db=db, product=product)
            created_products.append(created_product)
        db.commit()
        return {
            "message": "Products uploaded successfully",
            "count": len(created_products)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload products: {str(e)}")
