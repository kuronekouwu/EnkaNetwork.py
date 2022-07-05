# Info library
VERSION = "1.2.0"
AUTHOR = "M-307"

# Base URL
BASE_URL = "https://enka.shinshin.moe/{PATH}"

def create_path(path: str) -> str:
    return BASE_URL.format(PATH=path)

def create_ui_path(filename: str) -> str:
    return create_path(f"ui/{filename}.png")

def validate_uid(uid: str) -> bool:
    return len(uid) == 9 and uid.isdigit() and 100000000 < int(uid) < 999999999