# data_manager.py
# ========================
# This module provides a simple game data manager for saving and loading structured game data.
# Features:
# - Section-based structure (like INI files)
# - Optional encryption using Fernet (symmetric encryption)
# - Human-readable file format when not encrypted
# - Easy access to nested data via sections and keys

import os
import ast
from cryptography.fernet import Fernet

# Path to the encryption key file
KEY_PATH = "secret.key"

# Function to retrieve the encryption key, or create one if it doesn't exist
def get_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, 'wb') as f:
            f.write(key)
        return key
    with open(KEY_PATH, 'rb') as f:
        return f.read()

# Global cipher object used for encryption/decryption
CIPHER = Fernet(get_key())

# Serialize a dictionary into a custom text format
def _serialize(data: dict) -> str:
    lines = []
    for section, section_data in data.items():
        lines.append(f"[{section}]")  # Section header
        for key, value in section_data.items():
            lines.append(f"{key} = {repr(value)}")  # Save key-value pairs with Python repr()
        lines.append("")  # Blank line between sections
    return "\n".join(lines)

# Deserialize text back into a nested dictionary
def _deserialize(raw: str) -> dict:
    db = {}
    current_section = None
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # Skip blank lines and comments
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]  # New section
            db[current_section] = {}
        elif "=" in line and current_section:
            key, val = line.split("=", 1)
            try:
                # Try to convert string to a Python literal (list, int, tuple, etc.)
                db[current_section][key.strip()] = ast.literal_eval(val.strip())
            except Exception:
                # Fallback to raw string if eval fails
                db[current_section][key.strip()] = val.strip()
    return db

# GameDB is the main class to load, access, modify, and save game data
class GameDB:
    def __init__(self, path: str, encrypt: bool = False):
        self.path = path           # Path to the save file
        self.encrypt = encrypt     # Whether to use encryption
        self.data = {}             # Internal dictionary to hold the game data

        # Auto-load the file if it already exists
        if os.path.exists(path):
            self.load()

    # Load the file from disk, and decrypt if needed
    def load(self):
        with open(self.path, 'rb') as f:
            head = f.readline()
            if head == b"ENCRYPTED\n":
                # File is encrypted: decrypt content
                content = CIPHER.decrypt(f.read()).decode()
            else:
                # File is plain text: rewind and read normally
                f.seek(0)
                content = f.read().decode()
        self.data = _deserialize(content)

    # Save current data to disk, with optional encryption
    def save(self):
        text = _serialize(self.data)
        if self.encrypt:
            with open(self.path, 'wb') as f:
                f.write(b"ENCRYPTED\n")  # Header to identify encrypted files
                f.write(CIPHER.encrypt(text.encode()))
        else:
            with open(self.path, 'w') as f:
                f.write(text)

    # Get a value from the data safely
    def get(self, section, key, default=None):
        return self.data.get(section, {}).get(key, default)

    # Set a value in the data (auto-creates sections if needed)
    def set(self, section, key, value):
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
