import base64
from broadcast.utils.crypto.aes import AESCBC
from broadcast.utils.common import bit_str_xor


class ElCipher():
    def __init__(self):
        self.aes_cbc = AESCBC

    def encrypt(self, key, raw, K):
        aes_cbc = self.aes_cbc(key=key)
        enc = aes_cbc.encrypt(raw)[:8]
        cipher_bit = bit_str_xor(enc, K)
        cipher_text = base64.b64encode(cipher_bit).decode()
        return cipher_text

    def decrypt(self, key, raw, cipher_text):
        aes_cbc = self.aes_cbc(key=key)
        enc = aes_cbc.encrypt(raw=raw)[:8]
        plaint_text = base64.b64decode(cipher_text.encode())
        K = bit_str_xor(enc, plaint_text)
        return K
