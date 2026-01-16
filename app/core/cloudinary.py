import cloudinary
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)
print("✅ Cloudinary configured.")

conf = cloudinary.config()
assert conf.api_key, "Cloudinary not configured"
