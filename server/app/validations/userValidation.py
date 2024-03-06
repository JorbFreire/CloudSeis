from re import search

def validateData(*expected_data: str, data: dict[str, str]) -> bool:
    return all(key in expected_data for key in data)

def emailRegex(email: str) -> bool:
    pattern = r"@([a-zA-Z0-9.-]+)\."
    if search(pattern, email):
        return True
    else:
        return False

def passwordRegex(password: str) -> bool:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
    if search(pattern, password):
        return True
    else:
        return False
