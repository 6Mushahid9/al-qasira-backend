from app.core.firebase import get_firestore
from app.models.product import ProductCreate, ProductUpdate
from app.services.image_service import upload_image, delete_image
from fastapi import UploadFile
import uuid

db = get_firestore()
COLLECTION = "products"

def create_product(product: ProductCreate, image: UploadFile):
    uid = str(uuid.uuid4())

    image_url = upload_image(image, uid)

    data = product.dict()
    data.update({
        "uid": uid,
        "image": image_url
    })

    db.collection(COLLECTION).document(uid).set(data)
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
        existing_image = data.get("image")
        if existing_image:
            delete_image(existing_image)
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
    image_url = data.get("image")
    if image_url:
        delete_image(image_url)

    doc_ref.delete()
    return True

def get_featured_products():
    return [
        doc.to_dict()
        for doc in db.collection(COLLECTION)
        .where("featured", "==", True)
        .stream()
    ]
