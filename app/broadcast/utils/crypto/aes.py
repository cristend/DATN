import os
import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Counter


class AESCBC():
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.md5(key).digest()

    def encrypt(self, raw, iv=None):
        if isinstance(raw, str):
            raw = raw.encode()
        raw = self.pad(raw)
        if not iv:
            iv = b'\x01'*16
        else:
            iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            plaintext = f.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + '.enc', 'wb') as f:
            f.write(enc)
        os.remove(file_name)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return (cipher.decrypt(enc[AES.block_size:]).
                rstrip(b'\0').decode())

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            ciphertext = f.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:4], 'wb') as f:
            f.write(dec)
        os.remove(file_name)

    def pad(self, s):
        return s + b'\0' * (AES.block_size - len(s) % AES.block_size)


class AESCTR():
    def __init__(self, key):
        self.key = hashlib.md5(key).digest()

    def encrypt(self, raw):
        if not isinstance(raw, bytes):
            raw = raw.encode()
        nonce = Random.new().read(8)
        counter = Counter.new(64, nonce)
        cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
        return base64.b64encode(nonce+cipher.encrypt(raw))

    def decrypt(self, enc):
        if not isinstance(enc, bytes):
            enc = enc.encode()
        enc = base64.b64decode(enc)
        nonce = enc[:8]
        counter = Counter.new(64, nonce)
        cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
        return cipher.decrypt(enc[8:])

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            plaintext = f.read()
        enc = self.encrypt(raw=plaintext)
        name, extension = file_name.split('.')
        with open(name + '.enc.' + extension, 'wb') as f:
            f.write(enc)
        return base64.b64encode(enc).decode()

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            ciphertext = f.read()
        dec = self.decrypt(enc=ciphertext)
        name, remove, extension = file_name.split('.')
        with open(name + '_copy.' + extension, 'wb') as f:
            f.write(dec)
