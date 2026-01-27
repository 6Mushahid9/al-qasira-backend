from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.firebase import init_firebase
from app.core.cloudinary import cloudinary
from app.core.session import add_session_middleware
from app.routes.admin_auth import router as admin_auth_router
from app.routes.product_routes import router as product_router
from app.routes.admin_routes import router as admin_router
from app.routes.note_routes import router as note_router
# from app.api.routes.dev_routes import router as dev_router

app = FastAPI(title=settings.APP_NAME)

# ✅ Middleware setup
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    # same_site="lax",
    # https_only=False      
    same_site="none",
    https_only=True      
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase once during startup
@app.on_event("startup")
def on_startup():
    init_firebase()
    print("🔥 Firebase ready and connected!")

# Routers
app.include_router(admin_auth_router)
app.include_router(product_router, prefix="/api", tags=["Products"])
app.include_router(admin_router, prefix="/api", tags=["Admin"])
app.include_router(note_router, prefix="/api", tags=["Notes"])
# app.include_router(dev_router)

# Root route
@app.get("/")
def root():
    return {"message": "Al-qasira API is running 🚀"}
