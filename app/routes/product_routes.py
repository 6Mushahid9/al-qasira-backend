# app/api/routes/product_routes.py

from fastapi import APIRouter, HTTPException, Query
from app.models.product import ProductResponse
from app.models.pagination import PaginatedResponse
from app.services.product_service import (
    get_all_products,
    get_product,
    get_featured_products,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=PaginatedResponse[dict])
def fetch_products(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
):
    return get_all_products(page=page, limit=limit)


@router.get("/featured", response_model=list[dict])
def fetch_featured_products():
    return get_featured_products()


@router.get("/{uid}", response_model=ProductResponse)
def fetch_product(uid: str):
    product = get_product(uid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product

