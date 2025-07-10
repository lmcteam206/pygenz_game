# data_manager.py

import os
import ast
from cryptography.fernet import Fernet

KEY_PATH = "secret.key"

def get_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, 'wb') as f:
            f.write(key)
        return key
    with open(KEY_PATH, 'rb') as f:
        return f.read()

CIPHER = Fernet(get_key())

def _serialize(data: dict) -> str:
    lines = []
    for section, section_data in data.items():
        lines.append(f"[{section}]")
        for key, value in section_data.items():
            lines.append(f"{key} = {repr(value)}")
        lines.append("")
    return "\n".join(lines)

def _deserialize(raw: str) -> dict:
    db = {}
    current_section = None
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]
            db[current_section] = {}
        elif "=" in line and current_section:
            key, val = line.split("=", 1)
            try:
                db[current_section][key.strip()] = ast.literal_eval(val.strip())
            except Exception:
                db[current_section][key.strip()] = val.strip()
    return db

class GameDB:
    def __init__(self, path: str, encrypt: bool = False):
        self.path = path
        self.encrypt = encrypt
        self.data = {}

        if os.path.exists(path):
            self.load()

    def load(self):
        with open(self.path, 'rb') as f:
            head = f.readline()
            if head == b"ENCRYPTED\n":
                content = CIPHER.decrypt(f.read()).decode()
            else:
                f.seek(0)
                content = f.read().decode()
        self.data = _deserialize(content)

    def save(self):
        text = _serialize(self.data)
        if self.encrypt:
            with open(self.path, 'wb') as f:
                f.write(b"ENCRYPTED\n")
                f.write(CIPHER.encrypt(text.encode()))
        else:
            with open(self.path, 'w') as f:
                f.write(text)

    def get(self, section, key, default=None):
        return self.data.get(section, {}).get(key, default)

    def set(self, section, key, value):
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
