from pydantic import BaseModel
from typing import List, Optional
from app.models.product_volume import ProductVolume
from app.models.product_notes import ProductNotes
from pydantic import Field


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
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)

    tags: Optional[List[str]] = None
    category: Optional[str] = None
    featured: Optional[bool] = None

    volumes: Optional[List[ProductVolume]] = None
    notes: Optional[ProductNotes] = None

    class Config:
        extra = "forbid"   # ⬅️ prevents silent garbage fields


class ProductResponse(ProductBase):
    uid: str


class BulkDeleteRequest(BaseModel):
    uids: List[str]
