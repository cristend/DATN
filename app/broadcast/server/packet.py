import pdb
import os
import base64
from Crypto import Random
from . import bt, labels
from .functions import _find_subsets, get_key
from broadcast.utils.common import bit_str_xor
from broadcast.utils.crypto.aes import AESCTR
from broadcast.utils.crypto.EL import ElCipher

revokes = [9, 10, 14, 15]
st = bt.get_ST(revokes=revokes)
subsets = _find_subsets(root=st)
subsets_key = get_key(subsets=subsets, labels=labels)
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
PATH_FILE = 'media/test.txt'
path = os.path.abspath(os.getcwd())
file_name = os.path.join(path, PATH_FILE)
# part of packet
body = ''
header = ''
packet = ''
# Body
body = aes_ctr.encrypt_file(file_name=file_name)
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
pdb.set_trace()
