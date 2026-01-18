from fastapi import Request, HTTPException, status
from app.core.security import is_admin_authenticated

def admin_required(request: Request):
    if not is_admin_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required"
        )
