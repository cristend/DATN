import base64
from src.common.resource import bit_str_xor
from src.crypto.FK import FkCipher
from src.crypto.EL import ElCipher
from src.crypto.EL_xor import ELxorCipher


class BroadCast():
    def __init__(self, K, subset_keys={}):
        self.K = K
        self.F_K = FkCipher(K=K)
        self.E_L = ElCipher()
        self.subset_keys = subset_keys

    def packet(self, msg, U):
        # Create packet send to user, keys is dictionary which have keys as
        # index of subset cover and values are key of this subset
        index_list = list(self.subset_keys.keys())
        # key_list = list(self.subset_keys.values())
        # K = BitArray(bytes=K).bin
        body = self.F_K.encrypt(msg=msg)
        header = ','.join(index_list) + ',' + base64.b64encode(U).decode()
        cipher_list = list()
        packet = ''

        for index in index_list:
            ll_key = self.subset_keys[index]
            index_bytes = index.encode()
            raw = bit_str_xor(left=U, right=index_bytes)
            ll_key_cipher = self.E_L.encrypt(key=ll_key, raw=raw)
            el = ELxorCipher(cipher=ll_key_cipher)
            subset_cipher = el.encrypt(key=self.K)
            cipher_list.append(subset_cipher)
        header = header + ',' + ','.join(cipher_list)
        packet = '[' + header + '],' + body
        return packet
