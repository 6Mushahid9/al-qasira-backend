from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.core.security import verify_password

router = APIRouter(prefix="/auth", tags=["Admin Auth"])

class LoginRequest(BaseModel):
    password: str


@router.post("/login")
async def admin_login(request: Request, body: LoginRequest):
    admin_hash = settings.ADMIN_PASSWORD_HASH
    if not admin_hash or not verify_password(body.password, admin_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    request.session["is_admin"] = True
    return {"message": "Admin authenticated"}


@router.get("/me")
async def admin_me(request: Request):
    if request.session.get("is_admin"):
        return {"admin": True}
    raise HTTPException(status_code=401, detail="Not authenticated")


@router.post("/logout")
async def admin_logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}