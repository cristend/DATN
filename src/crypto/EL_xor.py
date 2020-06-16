from src.common.resource import bit_str_xor
import base64
from bitstring import BitArray


FIXED_LENGTH = 56


class ELxorCipher():
    def __init__(self, cipher):
        # cipher of E_L cipher with key is ll_key and raw is U xor index
        self.cipher = cipher

    def encrypt(self, key):
        # key is secret key K
        prefix_K = BitArray(bytes=base64.b64decode(
            self.cipher)).bin[:FIXED_LENGTH]
        # encrypt by xor
        enc = bit_str_xor(prefix_K, key)
        # convert base64
        cipher = base64.b64encode(BitArray(bin=enc).bytes).decode()
        return cipher

    def decrypt(self, key):
        # key is cipher of encrypt
        key = base64.b64decode(key.encode())
        # decode base64
        dec = BitArray(bytes=base64.b64decode(self.cipher.encode())).bin
        # take K first bit
        prefix_K = BitArray(bin=dec[:FIXED_LENGTH]).bytes
        # convert to bit string plaintext is secret K
        plaintext = BitArray(bytes=bit_str_xor(prefix_K, key)).bin
        return plaintext
