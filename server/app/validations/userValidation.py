from re import search

from ..errors.AppError import AppError

def validateData(*expected_data: str, data: dict[str, str]) -> AppError | None:
    if not all(key in expected_data for key in data):
        raise AppError("Invalide body", 401)

def credentialsRegex(email: str, password: str) -> AppError | None:
    emailPattern = r"@([a-zA-Z0-9.-]+)\." 
    passwordPattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

    if not search(emailPattern, email) or not search(passwordPattern, password):
        raise AppError("Invalid Credentials", 401)
