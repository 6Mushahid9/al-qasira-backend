from pydantic import BaseModel
from typing import List


class ProductNotes(BaseModel):
    top: List[str]      # note UIDs
    middle: List[str]
    base: List[str]
