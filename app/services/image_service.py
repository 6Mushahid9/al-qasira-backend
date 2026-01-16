from fastapi import UploadFile
import cloudinary.uploader

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}

def upload_image(file: UploadFile, uid: str) -> str:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise RuntimeError(
            f"Invalid image type '{file.content_type}'. "
            "Only JPG, PNG, WEBP are allowed."
        )

    try:
        file.file.seek(0)  # 🔑 VERY IMPORTANT

        result = cloudinary.uploader.upload(
            file.file,
            folder=f"products/{uid}",
            resource_type="image"
        )

        return result["secure_url"]

    except Exception as e:
        raise RuntimeError(f"Image upload failed: {str(e)}")



def delete_image(image_url: str):
    try:
        public_id = image_url.split("/upload/")[1].split(".")[0]
        print("DELETE DEBUG →", public_id)
        cloudinary.uploader.destroy(public_id)
        print("Image deleted from Cloudinary.")
    except Exception:
        # Silent fail – product deletion should not break
        pass
