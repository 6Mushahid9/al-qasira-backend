from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Depends,
)
from app.models.note import NoteCreate, NoteUpdate, NoteResponse
from app.services.note_service import (
    create_note,
    get_all_notes,
    update_note,
    delete_note,
)
from app.core.auth_middleware import admin_required

router = APIRouter()


@router.post(
    "/notes",
    response_model=NoteResponse,
    status_code=201,
    dependencies=[Depends(admin_required)],
)
def add_note(
    name: str = Form(...),
    image: UploadFile = File(...),
):
    note = NoteCreate(name=name, image="")
    return create_note(note, image)


@router.get(
    "/notes",
    response_model=list[NoteResponse],
)
def fetch_notes():
    return get_all_notes()


@router.put(
    "/notes/{uid}",
    response_model=NoteResponse,
    dependencies=[Depends(admin_required)],
)
def edit_note(
    uid: str,
    updates: NoteUpdate = Form(...),
    image: UploadFile | None = File(None),
):
    note = update_note(uid, updates, image)
    if not note:
        raise HTTPException(404, "Note not found.")
    return note


@router.delete(
    "/notes/{uid}",
    status_code=204,
    dependencies=[Depends(admin_required)],
)
def remove_note(uid: str):
    if not delete_note(uid):
        raise HTTPException(404, "Note not found.")


