import base64
from bitstring import BitArray
from src.crypto.ggm import PRNG
from src.common.resource import byte_xor


class FkCipher():
    def __init__(self, K):
        self.K = K

    def encrypt(self, msg, key):
        session_key = PRNG(seed=self.K, output_size=len(msg))
        session_key = bytes(BitArray(bin=session_key))
        enc = byte_xor(left=session_key, right=msg)
        cipher = base64.b64encode(enc).decode()
        return cipher

    def decrypt(self, cipher, key):
        enc = base64.b64decode(cipher.encode())
        session_key = PRNG(seed=self.K, output_size=len(enc))
        session_key = bytes(BitArray(bin=session_key))
        msg = byte_xor(left=session_key, right=enc)
        return msg
