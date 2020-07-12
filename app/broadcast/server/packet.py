# import os
import base64
from Crypto import Random
from . import bt, labels
from .functions import _find_subsets, get_key
from ..utils.common import bit_str_xor
from ..utils.crypto.aes import AESCTR
from ..utils.crypto.EL import ElCipher
from ..utils.crypto.ggm import G_M


def create_packet(revokes, data):
    st = bt.get_ST(revokes=revokes)
    subsets = _find_subsets(root=st)
    if subsets:
        subsets_key = get_key(subsets=subsets, labels=labels)
    else:
        if subsets is None:
            subsets_key = {'none': Random.new().read(32)}
        else:
            subsets_key = {'00': G_M(labels[0])}
    index_list = list(subsets_key.keys())
    # --- init ---
    # sesssion key K
    K = Random.new().read(8)
    # random salt
    U = Random.new().read(16)
    # F_K as aes_ctr mode
    aes_ctr = AESCTR(key=K)
    # E_L as aes_cbc mode with special implement
    E_L = ElCipher()
    # msg to broadcast
    # PATH_FILE = 'media/test.txt'
    # path = os.path.abspath(os.getcwd())
    # file_name = os.path.join(path, PATH_FILE)
    # part of packet
    body = ''
    header = ''
    packet = ''
    # Body
    body = aes_ctr.encrypt(raw=data).decode()
    # Header
    cipher_list = list()
    header = ','.join(index_list) + ',' + base64.b64encode(U).decode()
    for index in index_list:
        ll_key = subsets_key[index]
        index_bytes = index.encode()
        raw = bit_str_xor(left=U, right=index_bytes)
        subset_cipher = E_L.encrypt(key=ll_key, raw=raw, K=K)
        cipher_list.append(subset_cipher)
    header = header + ',' + ','.join(cipher_list)
    # Packet
    packet = '[' + header + '],' + body
    return packet
