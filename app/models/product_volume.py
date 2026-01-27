from pydantic import BaseModel


class ProductVolume(BaseModel):
    volumeML: int    # e.g. 100, 300, 500
    price: int       # price for that volume
