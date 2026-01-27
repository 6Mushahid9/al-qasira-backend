# use this no make new passwork hash.
# make password, place hash in env and restart server to use new password



# import os
# import hashlib
# import base64
# from fastapi import APIRouter

# router = APIRouter(prefix="/dev", tags=["dev"])

# ITERATIONS = 29000


# def hash_password(password: str) -> str:
#     salt = os.urandom(16)
#     dk = hashlib.pbkdf2_hmac(
#         "sha256",
#         password.encode(),
#         salt,
#         ITERATIONS
#     )
#     return (
#         f"$pbkdf2-sha256${ITERATIONS}$"
#         f"{base64.b64encode(salt).decode()}$"
#         f"{base64.b64encode(dk).decode()}"
#     )


# @router.get("/hash")
# def generate_hash(password: str):
#     return {
#         "password": password,
#         "hash": hash_password(password)
#     }
