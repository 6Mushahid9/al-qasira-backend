from fastapi import UploadFile
from app.core.firebase import get_firestore
from app.models.product import ProductCreate, ProductUpdate
from app.services.image_service import upload_image, delete_image

db = get_firestore()
COLLECTION = "products"


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
