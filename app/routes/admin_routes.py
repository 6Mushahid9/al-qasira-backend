# app/api/routes/admin_product_routes.py

from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
    Form,
    Depends,
    Query,
)
from typing import Optional
import json
from pydantic import ValidationError

from app.models.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    BulkDeleteRequest,
    FeaturedUpdate,
)
from app.models.pagination import PaginatedResponse
from app.services.admin_service import (
    get_all_admin_products,
    create_product,
    update_product,
    delete_product,
    bulk_delete_products,
    toggle_product_featured,
)
from app.core.auth_middleware import admin_required

router = APIRouter(
    prefix="/admin", tags=["Admin"],
    dependencies=[Depends(admin_required)],
)

@router.get("", response_model=PaginatedResponse[dict])
def fetch_products(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    q: str | None = Query(None),
):
    return get_all_admin_products(
        page=page,
        limit=limit,
        q=q,
    )


@router.post("", response_model=ProductResponse, status_code=201)
def add_product(
    name: str = Form(...),
    description: str = Form(...),
    tags: list[str] = Form(...),       # JSON string
    category: str = Form(...),
    featured: bool = Form(False),
    volumes: str = Form(...),    # JSON string
    notes: str = Form(...),      # JSON string
    image: UploadFile = File(...),
):
    try:
        product = ProductCreate(
            name=name,
            description=description,
            tags=tags,
            category=category,
            featured=featured,
            volumes=json.loads(volumes),
            notes=json.loads(notes),
        )
        return create_product(product, image)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON in tags, volumes, or notes.",
        )

@router.patch("/{uid}/toggle-featured", response_model=ProductResponse)
def toggle_featured(uid: str):
    print("Toggling featured for product:", uid)
    product = toggle_product_featured(uid)

    if not product:
        raise HTTPException(404, "Product not found")

    return product


@router.patch("/{uid}", response_model=ProductResponse)
def edit_product(
    uid: str,
    updates: str = Form(...),
    image: UploadFile | None = File(None),
):
    try:
        update_data = ProductUpdate(**json.loads(updates))
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON in update payload.")
    except ValidationError as e:
        raise HTTPException(422, detail=e.errors())

    product = update_product(uid, update_data, image)
    if not product:
        raise HTTPException(404, "Product not found.")

    return product

@router.delete("/bulk")
def bulk_delete(payload: BulkDeleteRequest):
    if not payload.uids:
        raise HTTPException(
            status_code=400,
            detail="uids list cannot be empty.",
        )

    result = bulk_delete_products(payload.uids)
    return {
        "message": "Bulk delete completed.",
        **result,
    }


@router.delete("/{uid}", status_code=204)
def remove_product(uid: str):
    if not delete_product(uid):
        raise HTTPException(status_code=404, detail="Product not found.")


