# app/services/product_service.py
from app.core.firebase import get_firestore
from app.models.product import ProductCreate, ProductUpdate
from app.services.image_service import upload_image, delete_image
from fastapi import UploadFile

db = get_firestore()
COLLECTION = "products"

def create_product(product: ProductCreate, image: UploadFile):
    doc_ref = db.collection(COLLECTION).document()
    uid = doc_ref.id

    image_url = upload_image(image, uid)

    data = product.dict()
    data.update({
        "uid": uid,
        "image": image_url
    })

    doc_ref.set(data)
    return data

def get_all_products():
    return [doc.to_dict() for doc in db.collection(COLLECTION).stream()]

def get_product(uid: str):
    doc = db.collection(COLLECTION).document(uid).get()
    return doc.to_dict() if doc.exists else None

def update_product(uid: str, updates: ProductUpdate, image: UploadFile | None):
    doc_ref = db.collection(COLLECTION).document(uid)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    data = doc.to_dict() or {}

    if image:
        if data.get("image"):
            delete_image(data["image"])
        data["image"] = upload_image(image, uid)

    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    data.update(update_data)

    doc_ref.set(data)
    return data

def delete_product(uid: str):
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
    deleted = []
    not_found = []

    batch = db.batch()

    for uid in uids:
        doc_ref = db.collection(COLLECTION).document(uid)
        doc = doc_ref.get()

        if not doc.exists:
            not_found.append(uid)
            continue

        data = doc.to_dict() or {}
        image_url = data.get("image")

        if image_url:
            delete_image(image_url)

        batch.delete(doc_ref)
        deleted.append(uid)

    batch.commit()

    return {
        "deleted": deleted,
        "not_found": not_found,
        "deleted_count": len(deleted),
    }

def get_featured_products():
    return [
        doc.to_dict()
        for doc in db.collection(COLLECTION)
        .where("featured", "==", True)
        .stream()
    ]
