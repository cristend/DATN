import base64
from src.crypto.ggm import G_M
from src.common.resource import bit_str_xor
from src.crypto.EL import ElCipher
from src.crypto.EL_xor import ELxorCipher
from src.crypto.FK import FkCipher


class Receiver():
    def __init__(self, labels):
        self.labels = labels
        self.el = ElCipher()

    def find_id(self, ids):
        label_ids = list(self.labels.keys())
        id = (set(label_ids) & set(ids))
        return id.pop() if id else None

    def find_key(self, id):
        label = self.labels[id]
        return G_M(label)

    def mapping(self, ids, ciphers):
        _map = dict()
        for id, cipher in zip(ids, ciphers):
            _map[id] = cipher
        return _map

    def unpack(self, packet):
        header, body = packet.split('[')[1].split(']')
        header = header.split(',')
        split_index = int(len(header)/2)
        ids, U, ciphers = (
            header[:split_index],
            header[split_index:split_index+1].pop(),
            header[split_index+1:])
        cipher_dict = self.mapping(ids=ids, ciphers=ciphers)
        id = self.find_id(ids=ids)
        if id is None:
            return None
        ll_key = self.find_key(id=id)
        U = base64.b64decode(U.encode())
        el_raw = bit_str_xor(left=U, right=id.encode())
        subset_cipher = self.el.encrypt(key=ll_key, raw=el_raw)
        el_xor = ELxorCipher(cipher=subset_cipher)
        K = el_xor.decrypt(key=cipher_dict[id])
        F_K = FkCipher(K=K)
        msg = F_K.decrypt(cipher=body)
        return msg
