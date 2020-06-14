import os
import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher():
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.md5(key.encode()).digest()

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            plaintext = f.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + '.enc', 'wb') as f:
            f.write(enc)
        os.remove(file_name)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        import pdb
        pdb.set_trace()
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return (cipher.decrypt(enc[AES.block_size:]).
                rstrip(b'\0').decode('utf-8'))

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            ciphertext = f.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:4], 'wb') as f:
            f.write(dec)
        os.remove(file_name)

    def pad(self, s):
        return s+'\0' * (AES.block_size - len(s) % AES.block_size)
