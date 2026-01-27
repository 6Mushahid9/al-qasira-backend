from fastapi import UploadFile
from app.core.firebase import get_firestore
from app.services.image_service import upload_image, delete_image
from app.models.note import NoteCreate, NoteUpdate

db = get_firestore()
COLLECTION = "notes"


def create_note(note: NoteCreate, image: UploadFile):
    doc_ref = db.collection(COLLECTION).document()
    uid = doc_ref.id

    image_url = upload_image(image, uid)

    data = note.dict()
    data.update({
        "uid": uid,
        "image": image_url,
    })

    doc_ref.set(data)
    return data


def get_all_notes():
    return [
        doc.to_dict()
        for doc in db.collection(COLLECTION)
        .order_by("name")
        .stream()
    ]


def update_note(uid: str, updates: NoteUpdate, image: UploadFile | None):
    doc_ref = db.collection(COLLECTION).document(uid)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    data = doc.to_dict() or {}

    # Handle image update
    if image:
        if data.get("image"):
            delete_image(data["image"])
        data["image"] = upload_image(image, uid)

    # Handle partial field updates
    update_data = {
        k: v for k, v in updates.dict(exclude_none=True).items()
    }

    data.update(update_data)
    doc_ref.set(data)

    return data



def delete_note(uid: str):
    doc_ref = db.collection(COLLECTION).document(uid)
    doc = doc_ref.get()

    if not doc.exists:
        return False

    data = doc.to_dict() or {}
    if data.get("image"):
        delete_image(data["image"])

    doc_ref.delete()
    return True


