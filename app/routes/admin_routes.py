# app/api/routes/admin_product_routes.py

from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
    Form,
    Depends,
)
from typing import Optional
import json
from pydantic import ValidationError

from app.models.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    BulkDeleteRequest,
)
from app.services.admin_service import (
    create_product,
    update_product,
    delete_product,
    bulk_delete_products,
)
from app.core.auth_middleware import admin_required

router = APIRouter(
    prefix="/admin", tags=["Admin"],
    dependencies=[Depends(admin_required)],
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


