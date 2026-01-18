# Session middleware setup

from starlette.middleware.sessions import SessionMiddleware

def add_session_middleware(app, secret_key: str):
    app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
        same_site="lax",
        https_only=True 
    )
