import base64
from src.crypto.aes import AESCipher


class ElCipher():
    def __init__(self, key):
        self.aes = AESCipher(key=key)

    def encrypt(self, raw):
        enc = self.aes.encrypt(raw).decode()
        cipher = base64.b64encode(enc).decode()
        return cipher

    def decrypt(self, cipher):
        dec = base64.b64decode(cipher.encode())
        plaintext = self.aes.decrypt(dec)
        return plaintext
