import secrets

def generate_short_code() -> str:
    return secrets.token_urlsafe(6)[:8]