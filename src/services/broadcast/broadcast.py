import base64
from bistring import BitArray
from Crypto import Random
from Crypto.Cipher import AES
from src.common.resource import byte_xor
from src.crypto.FK import FkCipher
from src.crypto.EL import ElCipher


class BroadCast():
    def __init__(self, K, msg, subset_keys={}):
        self.K = K
        self.F_K = FkCipher(K=self.K)
        self.E_L = ElCipher(key=None)
        self.subset_keys = subset_keys
        self.msg = msg

    def packet(self):
        # Create packet send to user, keys is dictionary which have keys as
        # index of subset cover and values are key of this subset
        index_list = list(self.subset_keys.keys())
        key_list = list(self.subset_keys.values())
        # K = BitArray(bytes=K).bin
        U = Random.new().read(AES.block_size)
        # U_bit_str = BitArray(bytes=U, length=AES.block_size*8).bin
        body = self.F_K.encrypt(msg=self.msg, key=self.K)
        header = ','.join(index_list) + base64.b64encode(U).decode()
        cipher_list = list()
        packet = ''

        for index in index_list:
            ll_key = key_list[index]
            index_bytes = index.encode()
            raw = byte_xor(left=U, right=index_bytes)
            # raw = bytes(BitArray(bin=raw_bit_str)).decode()
            cipherii = self.E_L.encrypt(key=ll_key, raw=raw)
            PrefixK = BitArray(bytes=base64.b64decode(
                cipherii)).bin[:len(self.K)]
            PrefixK = bytes(BitArray(bin=PrefixK))
            cipher = byte_xor(left=PrefixK, right=self.K)
            cipher = base64.b64encode(cipher).decode()
            cipher_list.append(cipher)
        header = header + ',' + ','.join(cipher_list)
        packet = '[' + header + '],' + body
        return packet
