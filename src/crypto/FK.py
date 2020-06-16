import base64
from arc4 import ARC4
from bitstring import BitArray
from src.crypto.ggm import PRNG
from src.common.resource import bit_str_xor, to_str


class FkCipher():
    def __init__(self, K):
        self.K = K

    # def encrypt(self, msg, flag=1):
    #     return (self.encrypt_bytes(msg=msg) if
    #             flag else self.encrypt_text(msg=msg))

    # def decrypt(self, cipher, flag=1):
    #     return (self.decrypt_bytes(cipher=cipher) if
    #             flag else self.decrypt_text(cipher=cipher))

    # def encrypt_bytes(self, msg):
    #     session_key = PRNG(seed=self.K, output_size=len(msg))
    #     session_key = BitArray(bin=session_key).bytes
    #     enc = bit_str_xor(left=session_key, right=msg)
    #     cipher = base64.b64encode(enc).decode()
    #     return cipher

    # def decrypt_bytes(self, cipher):
    #     enc = base64.b64decode(cipher.encode())
    #     session_key = PRNG(seed=self.K, output_size=len(enc))
    #     session_key = BitArray(bin=session_key).bytes
    #     msg = bit_str_xor(left=session_key, right=enc)
    #     return msg

    # def encrypt(self, msg):
    #     msg = msg.decode()
    #     msg = ''.join([bin(ord(x))[2:].zfill(8) for x in msg])
    #     session_key = PRNG(seed=self.K, output_size=len(msg))
    #     enc = bit_str_xor(left=msg, right=session_key)
    #     cipher = base64.b64encode(enc.encode()).decode()
    #     return cipher

    # def decrypt(self, cipher):
    #     dec = base64.b64decode(cipher.encode()).decode()
    #     session_key = PRNG(seed=self.K, output_size=len(dec))
    #     plaintext = bit_str_xor(left=dec, right=session_key)
    #     msg = to_str(plaintext)
    #     msg = msg.encode()
    #     return msg

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
