from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    image: str
    name: str
    description: str
    tags: List[str]
    pricePerML: str
    volumeML: int
    category: str
    featured: Optional[bool] = False

class ProductCreate(BaseModel):
    id: int
    name: str
    description: str
    tags: List[str]
    pricePerML: str
    volumeML: int
    category: str
    featured: Optional[bool] = False

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    pricePerML: Optional[str] = None
    volumeML: Optional[int] = None
    category: Optional[str] = None
    featured: Optional[bool] = None

class ProductResponse(ProductBase):
    uid: str
    id: int
