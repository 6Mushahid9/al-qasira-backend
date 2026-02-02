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
    get_note_by_id,
    update_note,
    delete_note,
)
from app.core.auth_middleware import admin_required
from typing import Optional

router = APIRouter(
    prefix="/notes", tags=["Notes"],
    dependencies=[Depends(admin_required)],
)

@router.post(
    "",
    response_model=NoteResponse,
    status_code=201,
)
def add_note(
    name: str = Form(...),
    image: UploadFile = File(...),
):
    note = NoteCreate(name=name, image="")
    return create_note(note, image)


@router.get(
    "",
    response_model=list[NoteResponse],
)
def fetch_notes():
    return get_all_notes()

@router.get(
    "/{uid}",
    response_model=NoteResponse,
)
def fetch_note(uid: str):
    note = get_note_by_id(uid)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")
    return note


@router.put(
    "/{uid}",
    response_model=NoteResponse,
)
def edit_note(
    uid: str,
    name: Optional[str] = Form(None),
    image: UploadFile | None = File(None),
):
    updates = NoteUpdate(name=name)
    note = update_note(uid, updates, image)

    if not note:
        raise HTTPException(404, "Note not found.")

    return note


@router.delete(
    "/{uid}",
    status_code=204,
)
def remove_note(uid: str):
    if not delete_note(uid):
        raise HTTPException(404, "Note not found.")


