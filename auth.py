# auth.py
# StatelessStates MVP - Secure Token Authentication (sample)

import os
import hashlib
import hmac
import base64
import time

# Generate a secret key (in production, store securely!)
SECRET_KEY = os.environ.get("SS_SECRET_KEY", "default_dev_key")

def generate_token(user_id: str, expires_in: int = 3600) -> str:
    """
    Generate a simple HMAC-based token.
    PQC-ready placeholder for integration with post-quantum algorithms.
    """
    expiry = int(time.time()) + expires_in
    msg = f"{user_id}:{expiry}".encode()
    signature = hmac.new(SECRET_KEY.encode(), msg, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(msg + b":" + signature).decode()
    return token

def validate_token(token: str) -> bool:
    """
    Validate a token and check expiry.
    """
    try:
        decoded = base64.urlsafe_b64decode(token.encode())
        user_id, expiry, signature = decoded.split(b":", 2)
        expiry = int(expiry)

        # Check expiry
        if expiry < int(time.time()):
            return False

        # Recreate signature
        msg = f"{user_id.decode()}:{expiry}".encode()
        expected_sig = hmac.new(SECRET_KEY.encode(), msg, hashlib.sha256).digest()

        return hmac.compare_digest(signature, expected_sig)
    except Exception:
        return False


# Example usage (for testing)
if __name__ == "__main__":
    tok = generate_token("user123")
    print("Generated:", tok)
    print("Valid?", validate_token(tok))
