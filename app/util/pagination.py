from math import ceil
from typing import List, TypeVar, Dict

T = TypeVar("T")


def paginate(
    *,
    items: List[T],
    page: int,
    limit: int,
    total_items: int
) -> Dict:
    """
    Pagination helper for NoSQL / list-based data sources.
    """

    if page < 1:
        page = 1

    if limit < 1:
        limit = 12

    total_pages = ceil(total_items / limit) if total_items else 1

    return {
        "data": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
    }
