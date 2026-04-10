import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class EncryptionUtil:
    def __init__(self, key: str):
        self.key = base64.b64decode(key)
        self.backend = default_backend()
    
    def encrypt(self, plaintext: str) -> str:
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + encrypted).decode('utf-8')
    
    def decrypt(self, ciphertext: str) -> str:
        data = base64.b64decode(ciphertext)
        iv = data[:16]
        encrypted_data = data[16:]
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        return decrypted.decode('utf-8')

# Test encryption
print("Testing encryption functionality...")

# Use the key from .env
key = "oO0rJX+bsEnhAyNDPNNaARCHXzCpLLbdw01VeNIlvto="

encryptor = EncryptionUtil(key)

# Test message
plaintext = "This is a test message with sensitive information"
print(f"Original: {plaintext}")

# Encrypt
encrypted = encryptor.encrypt(plaintext)
print(f"Encrypted: {encrypted}")

# Decrypt
decrypted = encryptor.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

if decrypted == plaintext:
    print("✓ Encryption/decryption working correctly!")
else:
    print("✗ Encryption/decryption failed!")
