import pytest  # noqa
import base64
from src.crypto.aes import AESCipher
from src.crypto.EL import ElCipher
from src.crypto.EL_xor import ELxorCipher
from src.crypto.FK import FkCipher


class TestCrypto():
    aes = AESCipher(key='test')
    el = ElCipher()
    fk = FkCipher(K='1001')
    cipher = base64.b64encode(b'this is a test').decode()
    elxor = ELxorCipher(cipher=cipher)

    def test_aes_cipher(self, aes=aes):
        msg = 'this is a test!'
        cipher = aes.encrypt(raw=msg)
        plaintext = aes.decrypt(enc=cipher)
        assert plaintext == msg

    def test_ElCipher(self, el=el):
        msg = 'this is a test!'
        cipher = el.encrypt(key='1001', raw=msg)
        plaintext = el.decrypt(key='1001', cipher=cipher)
        assert plaintext == msg

    def test_FkCipher(self, fk=fk):
        msg = 'this is a test'
        cipher = fk.encrypt(msg=msg)
        plaintext = fk.decrypt(cipher=cipher).decode()
        assert plaintext == msg

    def test_ELxorCipher(self, elxor=elxor):
        key = '10001001'
        cipher = elxor.encrypt(key=key)
        plaintext = elxor.decrypt(key=cipher)
        assert plaintext == key
