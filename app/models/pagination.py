from pydantic import BaseModel
from typing import Generic, List, TypeVar

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 1
    limit: int = 12


class PaginationMeta(BaseModel):
    page: int
    limit: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    pagination: PaginationMeta
