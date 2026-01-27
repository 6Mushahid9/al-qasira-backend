from pydantic import BaseModel
from typing import Optional


class NoteBase(BaseModel):
    name: str
    image: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None


class NoteResponse(NoteBase):
    uid: str
