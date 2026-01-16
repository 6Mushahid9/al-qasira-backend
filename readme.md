# ⚙️ Collab Hub Backend (FastAPI + Firebase)

This is the **backend** for the Collab Hub project — a scalable collaboration platform built using **FastAPI** and **Firebase**.  
It’s designed in a **modular structure**, so you can easily extend it later with authentication, APIs, database models, and more.

---

## 🧩 Project Overview

The backend handles:
- Environment configuration (via `.env`)
- Firebase Admin initialization
- API route management (future-ready)
- Core app startup using FastAPI

This structure ensures that adding new features like routes or database connections stays clean and consistent.

---

## 🏗️ Folder Structure
```markdown
server/
│
├── app/
│   ├── main.py              # Entry point of the FastAPI app
│   │
│   ├── core/                # Core configuration & global setup
│   │   ├── config.py        # Environment variables, app settings
│   │   ├── firebase.py      # Firebase Admin SDK initialization
│   │   └── __init__.py
│   │
│   ├── api/                 # (Future) API route folders
│   │   └── v1/
│   │       └── __init__.py
│   │
│   └── __init__.py
│
├── .env                     # Stores environment variables (not committed)
├── requirements.txt          # All required dependencies
└── venv/                     # Python virtual environment (ignored in Git)

```
---

## 🧩 Core Dependencies (Essential for Every FastAPI Project)

| Library                       | Purpose                                                         | Command                      |
| ----------------------------- | --------------------------------------------------------------- | ---------------------------- |
| **fastapi**                   | Main framework for building APIs                                | `pip install fastapi`        |
| **uvicorn**                   | ASGI server to run the FastAPI app                              | `pip install uvicorn`        |
| **python-dotenv**             | Loads environment variables from `.env`                         | `pip install python-dotenv`  |
| **fastapi[all]** *(optional)* | Installs FastAPI + extras like Pydantic and Starlette utilities | `pip install "fastapi[all]"` |
---

## 🧠 Developer Experience & Best Practices
| Library               | Purpose                                                       | Command                         |
| --------------------- | ------------------------------------------------------------- | ------------------------------- |
| **pydantic**          | Data validation and parsing (used in request/response models) | `pip install pydantic`          |
| **pydantic-settings** | Cleaner `.env` management via `BaseSettings` class            | `pip install pydantic-settings` |
| **PyJWT**             | JWT-based authentication                                      | `pip install PyJWT`             |
| **bcrypt / passlib**  | Password hashing and verification                             | `pip install bcrypt passlib`    |
| **black**             | Auto code formatter                                           | `pip install black`             |
| **isort**             | Auto import sorter                                            | `pip install isort`             |
| **flake8**            | Linting and code cleanliness                                  | `pip install flake8`            |



## 📘 File-by-File Explanation

### **`main.py`**
The main entry point of your backend app.

**Purpose:**
- Create the FastAPI instance
- Load configurations
- Initialize Firebase
- Register routes (in the future)
- Start the Uvicorn server

**Typical contents:**
```python
from fastapi import FastAPI
from app.core.config import settings
from app.core.firebase import firebase_app

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def read_root():
    return {"message": "Welcome to Collab Hub Backend!"}
````

---

### **`core/config.py`**

Handles app-wide configuration using **Pydantic Settings**.

**Purpose:**

* Load environment variables from `.env`
* Store project-level settings (like project name, CORS origins, Firebase paths)

**Example code:**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Collab Hub"
    FIREBASE_CREDENTIALS: str
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
```

---

### **`requirements.txt`**

List of dependencies used in this backend.
Install them with:

```bash
pip install -r requirements.txt
```

**Key Dependencies:**

| Dependency          | Purpose                            |
| ------------------- | ---------------------------------- |
| `fastapi`           | High-performance backend framework |
| `uvicorn`           | ASGI server to run FastAPI         |
| `firebase-admin`    | Firebase integration for backend   |
| `pydantic-settings` | Environment variable management    |
| `python-dotenv`     | Optional support for `.env` files  |
| `httpx`             | Async HTTP client for API calls    |

---

## ⚙️ Setup Instructions

### **1. Create a Virtual Environment**

```bash
python -m venv venv
```

### **2. Activate the Virtual Environment**

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Add Environment Variables**

Create a `.env` file inside the `server/` folder:

```
PROJECT_NAME=Collab Hub
FIREBASE_CREDENTIALS=serviceAccountKey.json
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### **5. Run the App**

```bash
uvicorn app.main:app --reload
```

### **6. Access the API**

* Base URL → [http://127.0.0.1:8000](http://127.0.0.1:8000)
* API Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧠 Future Scalability Plan

You can easily extend this backend by adding:

| Feature            | Description                       |
| ------------------ | --------------------------------- |
| `/api/v1/users`    | Manage users via Firebase Auth    |
| `/api/v1/projects` | Handle collaboration data         |
| `/api/v1/tasks`    | Store and manage user tasks       |
| Middleware         | Authentication, logging, CORS     |
| Database Layer     | Firestore, PostgreSQL, or MongoDB |
| WebSocket          | Real-time collaboration features  |

Each module will go inside its own folder under `app/api/v1/`.

---
# Connecting firebase

* made a firebase projec in firebase console, generated a new api key, it downloaded a file that i kept in root folder along with ".env" file.
* Then added it in env file.
* told about this new api key in config file

created a new file named *firebase.py* in folder - *core* and inserted below code:
```python

# app/core/firebase.py
import firebase_admin
from firebase_admin import credentials, firestore
import os

_firebase_app = None
_firestore_client = None

def init_firebase():
    """
    Initialize Firebase Admin SDK and Firestore client
    """
    global _firebase_app, _firestore_client
    if _firebase_app is not None:
        return _firebase_app, _firestore_client

    # Read service account path from environment variable
    sa_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "./serviceAccount.json")

    if not os.path.exists(sa_path):
        raise FileNotFoundError(f"Service account JSON not found at {sa_path}")

    cred = credentials.Certificate(sa_path)
    _firebase_app = firebase_admin.initialize_app(cred)
    _firestore_client = firestore.client()
    return _firebase_app, _firestore_client

def get_firestore():
    if _firestore_client is None:
        init_firebase()
    return _firestore_client

```

in main.py added this block:
```python

from app.core.firebase import init_firebase, get_firestore

@app.on_event("startup")
def startup_event():
    app, db = init_firebase()
    print("✅ Firebase connected:", db)
```
---
## Working with Schemas Services and Routes

✅ To build a User feature in FastAPI + Firebase, you’ll need 3 layers:

| Layer                  | File Example      | Purpose                                                                        | Folder          |
| ---------------------- | ----------------- | ------------------------------------------------------------------------------ | --------------- |
| **1️⃣ Schema / Model** | `user.py`         | Defines what a user looks like — fields, types, validation                     | `app/schemas/`  |
| **2️⃣ Service**        | `user_service.py` | Handles database operations (create, fetch, update, delete) and business logic | `app/services/` |
| **3️⃣ Route**          | `users.py`        | Exposes HTTP endpoints that call the service functions                         | `app/routers/`  |


Then in your app/main.py, you’ll import and include the router, like this:

```python
from app.routers import users

app.include_router(users.router)
```

Therefore the flow is — models → services → routes → main.py.

---

## Connecting to firebase

In google console see that it have Mail id given in serviceAccount.json file as "client_mail" and make sure it have roles: "Cloud Datastore User" & "Firebase Admin"

At this phase i was able to connect and add user in database
---
## 🧔 Author

**Mushahid Khisal Ansari**
*Collab Hub Backend (FastAPI + Firebase)*
GitHub: [http://github.com/6Mushahid9]

---