import base64
from arc4 import ARC4
from src.common.resource import bit_str_xor


class FkCipher():
    def __init__(self, K):
        self.K = K

    def encrypt(self, msg):
        if isinstance(msg, str):
            msg = msg.encode()
        stream_cipher = self.stream_enc(raw=msg)
        enc = bit_str_xor(left=msg, right=stream_cipher)
        cipher = base64.b64encode(enc).decode()
        return cipher

    def decrypt(self, cipher):
        dec = base64.b64decode(cipher.encode())
        stream_cipher = self.stream_enc(raw=dec)
        plaintext = bit_str_xor(dec, stream_cipher)
        return plaintext

    def stream_enc(self, raw):
        size = len(raw)
        session_key = b'\x01'*size
        arc4 = ARC4(self.K)
        stream_cipher = arc4.encrypt(session_key)
        return stream_cipher
