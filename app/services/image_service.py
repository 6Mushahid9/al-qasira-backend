# app/services/image_service.py
from fastapi import UploadFile
import cloudinary.uploader

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
FOLDER = "products"

def upload_image(file: UploadFile, public_id: str) -> str:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise RuntimeError(
            f"Invalid image type '{file.content_type}'. "
            "Allowed: JPG, PNG, WEBP."
        )

    try:
        file.file.seek(0)

        result = cloudinary.uploader.upload(
            file.file,
            folder=FOLDER,
            public_id=public_id,
            overwrite=True,
            resource_type="image"
        )
        return result["secure_url"]

    except Exception as e:
        raise RuntimeError(f"Image upload failed: {str(e)}")


def delete_image(image_url: str):
    try:
        public_id = image_url.split("/upload/")[1].rsplit(".", 1)[0]
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass
