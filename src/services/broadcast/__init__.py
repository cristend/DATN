import os
from Crypto import Random
from bitstring import BitArray
from .subet_label import SubsetLabel
from .subset_cover import SubsetCover
from ...server.binary_tree import Binary_tree
from ...server.steiner_tree import Steiner_tree
from .broadcast import BroadCast


KEY_SIZE = 56
PATH_FILE = 'media/test.txt'
path = os.path.abspath(os.getcwd())
file_name = os.path.join(path, PATH_FILE)
# msg
with open(file_name, 'rb') as f:
    msg = f.read()
# K
K = Random.new().read(KEY_SIZE)
K = BitArray(bytes=K).bin
# subset_keys
users = []
revokes = []
bt = Binary_tree().build(users=users)
st = Steiner_tree.build(revokes=revokes)
subset_cover = SubsetCover(bt=bt, st=st)
subset = subset_cover._find_subsets()
subset_label = SubsetLabel(subset=subset, bt=bt)
subset_keys = subset_label.get_key()
# broadcast
broadcast = BroadCast(K=K, msg=msg, subset_keys=subset_keys)
packet = broadcast.packet()
