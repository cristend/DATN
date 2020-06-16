import pytest  # noqa
import os
from Crypto import Random
from bitstring import BitArray
from src.services.users.receiver import Receiver
from src.common.resource import get_nodes
from src.server.binary_tree import Binary_tree
from src.user.users import Users
from src.services.broadcast.label import Label
from src.services.broadcast import BroadCast
from src.server.steiner_tree import Steiner_tree
from src.services.broadcast.subset_cover import SubsetCover
from src.services.broadcast.subet_label import SubsetLabel
from Crypto.Cipher import AES


class TestReceiver():
    users = Users()
    users = users.create_user(8)
    bt = Binary_tree().build(users=users)
    nodes = get_nodes(bt)
    user_node_list = [node for node in nodes if node.data is not None]
    user = user_node_list[3]
    label = Label(bt=bt)
    user_labels = label.get_user_labels(leaf=user)
    revoker = user_node_list[2]
    revoker_labels = label.get_user_labels(leaf=revoker)

    def test_unpack_user(self, labels=user_labels, bt=bt):
        revokes = ['10', '30', '70', '80']
        st = Steiner_tree(root=bt).build(revokes=revokes)
        subset_cover = SubsetCover(st=st, bt=bt)
        subsets = subset_cover._find_subsets()
        subset_label = SubsetLabel(subsets=subsets, bt=bt)
        subset_keys = subset_label.get_key()
        K = Random.new().read(7)
        K = BitArray(bytes=K).bin
        PATH_FILE = 'media/test.txt'
        path = os.path.abspath(os.getcwd())
        file_name = os.path.join(path, PATH_FILE)
        with open(file_name, 'rb') as f:
            msg = f.read()
        U = Random.new().read(AES.block_size)
        bc = BroadCast(K=K, subset_keys=subset_keys)
        packet = bc.packet(msg=msg, U=U)
        receiver = Receiver(labels=labels)
        unpack = receiver.unpack(packet=packet)
        assert unpack == msg

    def test_unpack_revoker(self, labels=revoker_labels, bt=bt):
        revokes = ['10', '30', '70', '80']
        st = Steiner_tree(root=bt).build(revokes=revokes)
        subset_cover = SubsetCover(st=st, bt=bt)
        subsets = subset_cover._find_subsets()
        subset_label = SubsetLabel(subsets=subsets, bt=bt)
        subset_keys = subset_label.get_key()
        K = Random.new().read(7)
        K = BitArray(bytes=K).bin
        PATH_FILE = 'media/test.txt'
        path = os.path.abspath(os.getcwd())
        file_name = os.path.join(path, PATH_FILE)
        with open(file_name, 'rb') as f:
            msg = f.read()
        U = Random.new().read(AES.block_size)
        bc = BroadCast(K=K, subset_keys=subset_keys)
        packet = bc.packet(msg=msg, U=U)
        receiver = Receiver(labels=labels)
        unpack = receiver.unpack(packet=packet)
        assert unpack is None
