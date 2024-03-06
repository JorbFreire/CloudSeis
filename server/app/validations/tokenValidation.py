from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

private_key = "private_key"
public_key = "public_key"

def generateToken(payload: dict, key: str) -> str | None:
    try:
        token = encode(payload=payload, key=key, algorithm="HS256")
    except Exception as e:
        print(e)
        return None

    return token

def verifyToken(token, key) -> bool:
    if not token:
        return False

    try:
        decode(token, key=key, algorithms=["HS256"])
    except InvalidSignatureError as e:
        print(f"Failed in token verification: {e}")
        return False
    except ExpiredSignatureError as e:
        print(f"Token out of validation {e}")
        return False

    return True

if __name__ == "__main__":
    pass
