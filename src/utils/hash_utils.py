import hashlib


def generate_input_hash(user_id: str, text: str) -> str:
    """
    Generate a SHA-256 hash based on the user_id and cleaned text input.
    """
    combined = f"{user_id}:{text.strip()}"
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()
