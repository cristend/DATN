import pytest  # noqa
import os
from Crypto import Random
from Crypto.Cipher import AES
from bitstring import BitArray
from src.server.binary_tree import Binary_tree
from src.server.steiner_tree import Steiner_tree
from src.user.users import Users
from src.common.resource import node_count, get_nodes
from src.services.broadcast.subset_cover import SubsetCover
from src.services.broadcast.subet_label import SubsetLabel
from src.services.broadcast.label import Label
from src.crypto.ggm import G_L, G_R, G_M
from src.services.broadcast import BroadCast
from src.crypto.EL import ElCipher
from src.crypto.FK import FkCipher
from src.crypto.EL_xor import ELxorCipher
from src.common.resource import bit_str_xor
from src.crypto.aes import AESCipher


class TestBroadCast():
    users = Users()
    users = users.create_user(8)
    bt = Binary_tree().build(users=users)
    # subset_label = SubsetLabel(subsets=subsets, bt=bt)
    nodes = get_nodes(bt)
    label_list = [node.label for node in nodes]
    user_node_list = [node for node in nodes if node.data is not None]
    # map_nodes = {1: nodes[0], 2: nodes[1], 3: nodes[8], 4: nodes[2],
    #              5: nodes[5], 6: nodes[9], 7: nodes[12], 8: nodes[3],
    #              9: nodes[4], 10: nodes[6], 11: nodes[7], 12: nodes[10],
    #              13: nodes[11], 14: nodes[13], 15: nodes[14]}

    def test_bt(self, bt=bt):
        # test number of node
        assert node_count(bt) == 15
        # test id of each node
        nodes = get_nodes(bt)
        true_list = ['1', '2', '4', '10', '20', '5',
                     '30', '40', '3', '6', '50', '60', '7', '70', '80']
        count = 0
        for node in nodes:
            assert node.id == true_list[count]
            count += 1

    def test_st(self, bt=bt):
        revokes = ['10', '30', '70', '80']
        st = Steiner_tree(root=bt).build(revokes=revokes)
        assert node_count(st) == 10
        nodes = get_nodes(st)
        true_list = ['1', '2', '4', '10', '5', '30', '3', '7', '70', '80']
        count = 0
        for node in nodes:
            assert node.id == true_list[count]
            count += 1

    def test_subset_cover(self, bt=bt):
        revokes = ['10', '30', '70', '80']
        st = Steiner_tree(root=bt).build(revokes=revokes)
        subset_cover = SubsetCover(st=st, bt=bt)
        subsets = subset_cover._find_subsets()
        true_list = ['37', '410', '530']
        assert_list = []
        for subset in subsets:
            id = subset.ancestor.id + subset.descendant.id
            assert_list.append(id)
        assert assert_list == true_list

    def test_label(self, bt=bt, label_list=label_list,
                   user_node_list=user_node_list, nodes=nodes):
        label = Label(bt=bt)
        # test get_user_labels
        user = user_node_list[1]
        root_label = label_list[0]
        second_label = label_list[1]
        four_label = label_list[2]
        S13 = G_R(root_label)
        S15 = G_R(G_L(root_label))
        S110 = G_L(G_L(G_L(root_label)))
        S25 = G_R(second_label)
        S210 = G_L(G_L(second_label))
        S410 = G_L(four_label)
        labels = label.get_user_labels(leaf=user)
        true_dict = {'13': S13, '15': S15, '110': S110,
                     '25': S25, '210': S210, '410': S410}
        assert labels == true_dict
        #  test get_labelij
        label13 = label.get_labelij(nodei=nodes[0], nodej=nodes[8])
        label15 = label.get_labelij(nodei=nodes[0], nodej=nodes[5])
        label410 = label.get_labelij(nodei=nodes[2], nodej=nodes[3])
        assert label13 == S13
        assert label15 == S15
        assert label410 == S410
        # test subset_label
        revokes = ['10', '30', '70', '80']
        st = Steiner_tree(root=bt).build(revokes=revokes)
        subset_cover = SubsetCover(st=st, bt=bt)
        subsets = subset_cover._find_subsets()
        subset_label = SubsetLabel(subsets=subsets, bt=bt)
        ll_keys = subset_label.get_key()
        third_label = label_list[8]
        five_label = label_list[5]
        S530 = G_L(five_label)
        S37 = G_R(third_label)
        true_dict = {'410': G_M(S410), '530': G_M(S530), '37': G_M(S37)}
        assert ll_keys == true_dict

    def test_broadcast(self, bt=bt):
        revokes = ['10', '30', '70', '80']
        st = Steiner_tree(root=bt).build(revokes=revokes)
        subset_cover = SubsetCover(st=st, bt=bt)
        subsets = subset_cover._find_subsets()
        subset_label = SubsetLabel(subsets=subsets, bt=bt)
        subset_keys = subset_label.get_key()
        index_list = list(subset_keys.keys())
        key_list = list(subset_keys.values())
        #
        K = Random.new().read(7)
        K = BitArray(bytes=K).bin
        # msg
        PATH_FILE = 'media/test.mp3'
        path = os.path.abspath(os.getcwd())
        file_name = os.path.join(path, PATH_FILE)
        with open(file_name, 'rb') as f:
            msg = f.read()
        # FK
        # E_L
            E_L = ElCipher()
            U = Random.new().read(AES.block_size)
            bc = BroadCast(K=K, subset_keys=subset_keys)
            packet = bc.packet(msg=msg, U=U)
            #
            header, body = packet.split('[')[1].split(']')

            # header_list = ['37', '410', '530', U,
            #                key_list[0], key_list[1], key_list[2]]
            assert_header_list = header.split(',')
            raw37 = bit_str_xor(left=U, right=index_list[0].encode())
            enc37 = E_L.encrypt(key=key_list[0], raw=raw37)
            el = ELxorCipher(cipher=enc37)
            assert_K = el.decrypt(key=assert_header_list[4])
            assert assert_K == K
            F_K = FkCipher(K=assert_K)
            assert_msg = F_K.decrypt(cipher=body)
            assert assert_msg == msg
            f.close()
