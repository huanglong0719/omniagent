import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from typing import Optional

class EncryptionUtil:
    def __init__(self, key: Optional[str] = None):
        if key:
            self.key = base64.b64decode(key)
        else:
            self.key = os.urandom(32)
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

    def get_key(self) -> str:
        return base64.b64encode(self.key).decode('utf-8')

# 单例实例
_encryption_util = None

def get_encryption_util() -> EncryptionUtil:
    global _encryption_util
    if not _encryption_util:
        from app.core.config import Config
        config = Config()
        key = config.get('ENCRYPTION_KEY')
        _encryption_util = EncryptionUtil(key)
    return _encryption_util
