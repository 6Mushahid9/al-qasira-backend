from pydantic import BaseModel
from typing import List, Optional
from app.models.product_volume import ProductVolume
from app.models.product_notes import ProductNotes


class ProductBase(BaseModel):
    image: str
    name: str
    description: str
    tags: List[str]
    category: str
    featured: bool = False

    volumes: List[ProductVolume]
    notes: ProductNotes


class ProductCreate(BaseModel):
    name: str
    description: str
    tags: List[str]
    category: str
    featured: bool = False

    volumes: List[ProductVolume]
    notes: ProductNotes


class ProductUpdate(BaseModel):
    image: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    featured: Optional[bool] = None

    volumes: Optional[List[ProductVolume]] = None
    notes: Optional[ProductNotes] = None


class ProductResponse(ProductBase):
    uid: str


class BulkDeleteRequest(BaseModel):
    uids: List[str]
