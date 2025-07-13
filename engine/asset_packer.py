import os
import struct

class SimpleAssetPacker:
    def __init__(self, key: bytes = b'\x42'):
        self.key = key

    def pack_folder(self, folder, output_file, encrypt=False):
        entries = []
        data_blob = b''

        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, folder).replace("\\", "/")
                with open(path, 'rb') as f:
                    raw = f.read()
                if encrypt:
                    raw = self._xor(raw)
                offset = len(data_blob)
                size = len(raw)
                data_blob += raw
                entries.append((rel_path, offset, size))

        with open(output_file, 'wb') as f:
            f.write(struct.pack("<I", len(entries)))
            for name, offset, size in entries:
                bname = name.encode('utf-8')
                f.write(struct.pack("<H", len(bname)))
                f.write(bname)
                f.write(struct.pack("<II", offset, size))
            f.write(data_blob)

        print(f"✅ Packed {len(entries)} files to '{output_file}'")

    def _xor(self, data: bytes) -> bytes:
        return bytes(b ^ self.key[i % len(self.key)] for i, b in enumerate(data))




packer = SimpleAssetPacker(key=b'my_key')
packer.pack_folder('assets', 'game_assets.pack', encrypt=True)


