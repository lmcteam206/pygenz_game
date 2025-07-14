# engine/personal_debug.py

import os
from datetime import datetime


class P_Debug:
    def __init__(self, log_dir="debug_logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        self.files = {
            "outputs": self._open_log("outputs.txt"),
            "engine": self._open_log("engine_bugs.txt"),
        }
        self.slots = {i: [] for i in range(1, 5)}
        for i in self.slots:
            self.files[f"slot{i}"] = self._open_log(f"slot{i}.txt")

    def _open_log(self, filename):
        return open(os.path.join(self.log_dir, filename), "a", encoding="utf-8")

    def _write(self, file_key, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        line = f"{timestamp} {message}\n"
        self.files[file_key].write(line)
        self.files[file_key].flush()

    def log_output(self, msg):
        self._write("outputs", msg)

    def add_engine_bug(self, bug):
        self._write("engine", bug)

    def add_to_slot(self, slot, item):
        if slot in self.slots:
            self.slots[slot].append(item)
            self._write(f"slot{slot}", item)
        else:
            print(f"Invalid slot: {slot}")

    def summary(self):
        print("=== Debug Summary ===")
        for key in self.files:
            path = os.path.join(self.log_dir, f"{key}.txt")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    count = sum(1 for _ in f)
                print(f"{key.capitalize()}: {count} lines")
            except FileNotFoundError:
                print(f"{key.capitalize()}: 0 lines")

    def __del__(self):
        for f in self.files.values():
            f.close()
