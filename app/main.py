from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.firebase import init_firebase
from app.core.cloudinary import cloudinary
from app.core.session import add_session_middleware
from app.api.routes.admin_auth import router as admin_auth_router
from app.api.routes.product_routes import router as product_router
# from app.api.routes.dev_routes import router as dev_router

app = FastAPI(title=settings.APP_NAME)

# ✅ Middleware setup
add_session_middleware(app, settings.SESSION_SECRET_KEY)
app.include_router(admin_auth_router)
# app.include_router(dev_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Initialize Firebase once during startup
@app.on_event("startup")
def on_startup():
    init_firebase()
    print("🔥 Firebase ready and connected!")

# ✅ Routers
app.include_router(product_router, prefix="/api", tags=["Products"])

# ✅ Root route
@app.get("/")
def root():
    return {"message": "Al-qasira API is running 🚀"}
