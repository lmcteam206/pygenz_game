import os
import shutil
import subprocess
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# === CONFIG ===
ENTRY_SCRIPT = "main.py"
ASSET_FOLDER = "assets"
ASSET_OUTPUT = "assets.dat"
SECRET_KEY = b"badass"
EXE_NAME = "game"

def encrypt_assets(folder, output_file, key):
    import io
    import zipfile

    print("📦 Packing and encrypting assets...")
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder)
                zipf.write(full_path, arcname)

    zip_data = zip_buffer.getvalue()
    key = sha256(key).digest()
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(zip_data, AES.block_size))

    with open(output_file, "wb") as f:
        f.write(bytes(cipher.iv) + encrypted)

    print(f"✅ Encrypted assets saved to {output_file}")

def build_exe():
    print("🛠️ Building EXE with PyInstaller...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--noconsole",  # Remove this if you want the console window
        f"--name={EXE_NAME}",
        f"--add-data={ASSET_OUTPUT};.",
        ENTRY_SCRIPT
    ], check=True)
    print(f"✅ Build complete. Output: dist/{EXE_NAME}.exe")

if __name__ == "__main__":
    encrypt_assets(ASSET_FOLDER, ASSET_OUTPUT, SECRET_KEY)
    build_exe()
