# app/api/routes/product_routes.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from app.models.product import ProductCreate, ProductUpdate, ProductResponse, BulkDeleteRequest
from app.services.product_service import *

router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=201)
def add_product(
    name: str = Form(...),
    description: str = Form(...),
    tags: List[str] = Form(...),
    pricePerML: str = Form(...),
    volumeML: int = Form(...),
    category: str = Form(...),
    featured: bool = Form(False),
    image: UploadFile = File(...)
):
    try:
        product = ProductCreate(
            name=name,
            description=description,
            tags=tags,
            pricePerML=pricePerML,
            volumeML=volumeML,
            category=category,
            featured=featured
        )
        return create_product(product, image)

    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to create product. Please try again later."
        )

@router.get("/products", response_model=List[ProductResponse])
def fetch_products():
    return get_all_products()

@router.get("/products/featured", response_model=List[ProductResponse])
def fetch_featured():
    return get_featured_products()

@router.get("/products/{uid}", response_model=ProductResponse)
def fetch_product(uid: str):
    product = get_product(uid)
    if not product:
        raise HTTPException(404, "Product not found.")
    return product

@router.put("/products/{uid}", response_model=ProductResponse)
def edit_product(
    uid: str,
    image: Optional[UploadFile] = File(None),
    updates: ProductUpdate = Form(...)
):
    product = update_product(uid, updates, image)
    if not product:
        raise HTTPException(404, "Product not found.")
    return product

@router.delete("/products/{uid}", status_code=204)
def remove_product(uid: str):
    if not delete_product(uid):
        raise HTTPException(404, "Product not found.")

@router.delete("/products/bulk")
def bulk_delete(payload: BulkDeleteRequest):
    if not payload.uids:
        raise HTTPException(
            status_code=400,
            detail="uids list cannot be empty."
        )

    result = bulk_delete_products(payload.uids)

    return {
        "message": "Bulk delete completed.",
        **result
    }