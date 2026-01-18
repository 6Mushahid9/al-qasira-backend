from app.core.config import settings
from fastapi import APIRouter, Request, HTTPException
from app.core.security import verify_password

router = APIRouter(prefix="/admin", tags=["Admin Auth"])

@router.post("/login")
async def admin_login(request: Request, password: str):
    admin_hash = settings.ADMIN_PASSWORD_HASH

    if not admin_hash or not verify_password(password, admin_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    request.session["is_admin"] = True
    return {"message": "Admin authenticated"}

@router.post("/logout")
async def admin_logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}
