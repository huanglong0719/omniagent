import base64
import os

# Generate a random 32-byte key for AES-256
key = os.urandom(32)
encoded_key = base64.b64encode(key).decode('utf-8')

print(f"Generated encryption key: {encoded_key}")
print("Please add this to your .env file as ENCRYPTION_KEY=")
