from src.crypto.aes import AESCipher


class ElCipher():
    def __init__(self):
        self.aes = AESCipher

    def encrypt(self, key, raw):
        aes = self.aes(key=key)
        cipher = aes.encrypt(raw).decode()
        return cipher

    def decrypt(self, key, cipher):
        aes = self.aes(key=key)
        plaintext = aes.decrypt(cipher.encode())
        return plaintext
