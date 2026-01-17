from app.core.config import settings
import firebase_admin
from firebase_admin import credentials, firestore

# ✅ Singleton variables
firebase_app = None
firestore_client = None


def init_firebase():
    """Initialize Firebase only once for the app lifecycle."""
    global firebase_app, firestore_client

    if firebase_app is not None and firestore_client is not None:
        return firestore_client

    # ✅ Build credentials from environment variables
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": settings.FIREBASE_PROJECT_ID,
        "client_email": settings.FIREBASE_CLIENT_EMAIL,
        "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
        "token_uri": "https://oauth2.googleapis.com/token",
    })

    firebase_app = firebase_admin.initialize_app(cred)
    firestore_client = firestore.client()

    print("✅ Firebase initialized successfully (env-based)")
    return firestore_client


def get_firestore():
    """Return initialized Firestore client (auto-init if needed)."""
    global firestore_client
    if firestore_client is None:
        return init_firebase()
    return firestore_client
