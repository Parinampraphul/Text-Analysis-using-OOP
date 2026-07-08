import hashlib
import hmac
import os


ITERATIONS = 260_000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_BYTES)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )
    return f"{ITERATIONS}${salt.hex()}${password_hash.hex()}"


def verify_password(password: str, stored_password: str) -> bool:
    try:
        iterations_text, salt_hex, hash_hex = stored_password.split("$", maxsplit=2)
        iterations = int(iterations_text)
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
    except ValueError:
        return False

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(password_hash, expected_hash)

