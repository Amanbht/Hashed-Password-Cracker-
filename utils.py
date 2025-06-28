import hashlib

def hash_string(password: str, algo: str) -> str:
    """
    Hashes a password string using the given algorithm.
    Supports: md5, sha1, sha256, sha512
    """
    algo = algo.lower()
    try:
        hashed = hashlib.new(algo)
        hashed.update(password.encode())
        return hashed.hexdigest()
    except ValueError:
        return None


def detect_hash_type(h: str) -> str:
    """
    Detects hash type based on length and character pattern.
    """
    h = h.strip().lower()
    if len(h) == 32 and all(c in "0123456789abcdef" for c in h):
        return "md5"
    elif len(h) == 40 and all(c in "0123456789abcdef" for c in h):
        return "sha1"
    elif len(h) == 64 and all(c in "0123456789abcdef" for c in h):
        return "sha256"
    elif len(h) == 128 and all(c in "0123456789abcdef" for c in h):
        return "sha512"
    else:
        return "unknown"


def is_possibly_salted(hash_value: str, cracked_result: str, algo: str) -> bool:
    """
    Heuristically determines if a hash may be salted:
    - We attempted cracking but got no result
    - Hash length looks valid
    - No exact match found from brute-force or dictionary

    NOTE: This is a basic check and doesn't guarantee salting.
    """
    if cracked_result is not None and cracked_result not in ["Not Found", "❌ Unknown Hash Format"]:
        return False  # Found a result, so it's not salted

    expected_length = {
        "md5": 32,
        "sha1": 40,
        "sha256": 64,
        "sha512": 128
    }.get(algo.lower())

    if expected_length is None:
        return False

    if len(hash_value.strip()) == expected_length:
        return True

    return False
