from app.core.firebase import get_firestore
from app.util.pagination import paginate

db = get_firestore()
COLLECTION = "products"


def get_all_products(page: int = 1, limit: int = 12):
    offset = (page - 1) * limit
    collection_ref = db.collection(COLLECTION)

    # 🔹 Total count (Firestore safe)
    total_items = len(list(collection_ref.stream()))

    # 🔹 Paginated query
    docs = (
        collection_ref
        .order_by("name")
        .offset(offset)
        .limit(limit)
        .stream()
    )

    items = []
    for doc in docs:
        data = doc.to_dict()
        if not data:
            continue

        items.append({
            "uid": data["uid"],
            "image": data.get("image", ""),
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "category": data.get("category", ""),
            "featured": data.get("featured", False),
            "tags": data.get("tags", []),
            "price_range": _get_price_range(data.get("volumes", [])),
        })

    return paginate(
        items=items,
        page=page,
        limit=limit,
        total_items=total_items,
    )


def get_product(uid: str):
    doc = db.collection(COLLECTION).document(uid).get()
    return doc.to_dict() if doc.exists else None


def get_featured_products():
    docs = (
        db.collection(COLLECTION)
        .where("featured", "==", True)
        .stream()
    )

    results = []
    for doc in docs:
        data = doc.to_dict()
        if not data:
            continue

        results.append({
            "uid": data["uid"],
            "image": data.get("image", ""),
            "name": data.get("name", ""),
            "category": data.get("category", ""),
            "tags": data.get("tags", []),
            "price_range": _get_price_range(data.get("volumes", [])),
        })

    return results


def _get_price_range(volumes: list[dict]) -> str:
    if not volumes:
        return ""

    prices = [v.get("price") for v in volumes if v.get("price") is not None]
    if not prices:
        return ""

    prices = [p for p in prices if p is not None]
    if not prices:
        return ""

    min_price = min(prices)
    max_price = max(prices)

    if min_price == max_price:
        return f"₹{min_price}"

    return f"₹{min_price} – ₹{max_price}"
