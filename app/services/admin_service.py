from fastapi import UploadFile
from app.core.firebase import get_firestore
from app.models.product import ProductCreate, ProductUpdate
from app.services.image_service import upload_image, delete_image
from app.util.pagination import paginate
from app.util.serializer import serialize_product_from_dict
from datetime import datetime


db = get_firestore()
COLLECTION = "products"

def get_all_admin_products(
    page: int = 1,
    limit: int = 12,
    q: str | None = None,
):
    offset = (page - 1) * limit
    collection_ref = db.collection(COLLECTION)

    query = collection_ref

    # 🔍 APPLY SEARCH FIRST
    if q:
        query = (
            query
            .order_by("name")
            .where("name", ">=", q)
            .where("name", "<=", q + "\uf8ff")
        )
    else:
        query = query.order_by("name")

    # 🔢 TOTAL COUNT (after search)
    total_items = len(list(query.stream()))

    # 📄 PAGINATION
    docs = (
        query
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
            "featured": data.get("featured", False),
        })

    return paginate(
        items=items,
        page=page,
        limit=limit,
        total_items=total_items,
    )


def create_product(product: ProductCreate, image: UploadFile):
    doc_ref = db.collection(COLLECTION).document()
    uid = doc_ref.id

    image_url = upload_image(image, uid)

    data = product.dict()
    data.update({
        "uid": uid,
        "image": image_url,
    })

    doc_ref.set(data)
    return data


def update_product(uid: str, updates: ProductUpdate, image: UploadFile | None):
    doc_ref = db.collection(COLLECTION).document(uid)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    update_payload = updates.dict(exclude_none=True)

    if image:
        old_image = (doc.to_dict() or {}).get("image")
        new_image = upload_image(image, uid)
        if old_image:
            delete_image(old_image)
        update_payload["image"] = new_image

    if update_payload:
        doc_ref.update(update_payload)

    return doc_ref.get().to_dict()

def serialize_product(doc) -> dict:
    data = doc.to_dict() or {}
    data.pop("uid", None)

    return {
        "uid": doc.id,
        **serialize_product_from_dict(data),
    }


# def update_product_featured(uid: str, featured: bool):
#     doc_ref = db.collection(COLLECTION).document(uid)
#     doc = doc_ref.get()

#     if not doc.exists:
#         return None

#     doc_ref.update({
#         "featured": featured,
#         "updated_at": datetime.utcnow(),
#     })

#     updated_doc = doc_ref.get()
#     return serialize_product(updated_doc)

def toggle_product_featured(uid: str):
    doc_ref = db.collection(COLLECTION).document(uid)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    current = (doc.to_dict() or {}).get("featured", False)
    print("Current featured status:", current)
    doc_ref.update({
        "featured": not current,
        # "updated_at": datetime.utcnow(),
    })
    print("Updated featured status:", not current)

    updated_doc = doc_ref.get()
    return serialize_product(updated_doc)


def delete_product(uid: str) -> bool:
    doc_ref = db.collection(COLLECTION).document(uid)
    doc = doc_ref.get()

    if not doc.exists:
        return False

    data = doc.to_dict() or {}

    if data.get("image"):
        delete_image(data["image"])

    doc_ref.delete()
    return True


def bulk_delete_products(uids: list[str]) -> dict:
    deleted, not_found = [], []
    batch = db.batch()

    for uid in uids:
        doc_ref = db.collection(COLLECTION).document(uid)
        doc = doc_ref.get()

        if not doc.exists:
            not_found.append(uid)
            continue

        data = doc.to_dict() or {}
        if data.get("image"):
            delete_image(data["image"])

        batch.delete(doc_ref)
        deleted.append(uid)

    batch.commit()

    return {
        "deleted": deleted,
        "not_found": not_found,
        "deleted_count": len(deleted),
    }
