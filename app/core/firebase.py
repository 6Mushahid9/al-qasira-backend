import firebase_admin
from firebase_admin import credentials, firestore
import os

# ✅ Singleton variables
firebase_app = None
firestore_client = None

def init_firebase():
    """Initialize Firebase only once for the app lifecycle."""
    global firebase_app, firestore_client

    if firebase_app is not None and firestore_client is not None:
        return firestore_client  # Already initialized

    sa_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "./serviceAccount.json")
    if not os.path.exists(sa_path):
        raise FileNotFoundError(f"❌ Service account JSON not found at {sa_path}")

    cred = credentials.Certificate(sa_path)
    firebase_app = firebase_admin.initialize_app(cred)
    firestore_client = firestore.client()

    print("✅ Firebase initialized successfully")
    return firestore_client


def get_firestore():
    """Return initialized Firestore client (auto-init if needed)."""
    global firestore_client
    if firestore_client is None:
        print("⚠️ Firestore not initialized — initializing now...")
        return init_firebase()
    return firestore_client
