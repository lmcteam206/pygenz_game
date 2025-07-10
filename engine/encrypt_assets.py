# encrypt_assets.py
import os
import zipfile
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256

ASSETS_FOLDER = "assets"
OUTPUT_FILE = "assets.dat"
KEY = b"badass"  # Change this!
KEY = sha256(KEY).digest()  # Make it exactly 32 bytes (AES-256)

def create_zip_bytes(folder):
    import io
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder)
                zipf.write(full_path, arcname)
    return zip_buffer.getvalue()

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return bytes(cipher.iv) + encrypted

zip_data = create_zip_bytes(ASSETS_FOLDER)
encrypted = encrypt_data(zip_data, KEY)
with open(OUTPUT_FILE, "wb") as f:
    f.write(encrypted)
print(f"✅ Encrypted asset file written to {OUTPUT_FILE}")