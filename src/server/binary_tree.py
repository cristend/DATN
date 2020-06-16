import math
import random
from src.server.node import Node
from src.common.resource import is_power

FIXED_SIZE = 4


class Binary_tree():
    def __init__(self):
        self.root = None

    def insert(self, node, depth, depth_leaf, id, user_list):
        if depth == depth_leaf-1:
            left_user = user_list.pop(0)
            right_user = user_list.pop(0)
            node.left = Node(id=left_user.id, data=left_user)
            node.left.parent = node
            node.right = Node(id=right_user.id, data=right_user)
            node.right.parent = node
            return None
        if node.left is None:
            left_id = 2*id
            node.left = Node(id=str(left_id))
            node.left.parent = node
            self.insert(node=node.left, depth=depth+1,
                        depth_leaf=depth_leaf, id=left_id, user_list=user_list)
        if node.right is None:
            right_id = 2*id + 1
            node.right = Node(id=str(right_id))
            node.right.parent = node
            self.insert(node=node.right, depth=depth+1,
                        depth_leaf=depth_leaf, id=right_id,
                        user_list=user_list)
        return None

    def set_label(self, node=None):
        node = self.root if node is None else node
        if node is None:
            return None
        node.label = format(random.getrandbits(
            FIXED_SIZE), 'b').zfill(FIXED_SIZE)
        if node.left:
            self.set_label(node=node.left)
        if node.right:
            self.set_label(node=node.right)

    def build(self, users=[]):
        # number of leaf in tree, should be a factor of 2.
        leafs = None
        # number of leaf padding if n is not a factor of 2
        # depth of a leaf
        depth_leaf = None
        # number of users, also as leafs if users is a factor of 2.
        n_users = len(users)
        if is_power(n_users, 2):
            depth_leaf = math.log(n_users, 2)
        else:
            leafs = 2**(int(math.log(n_users, 2)) + 1)
            depth_leaf = math.log(leafs, 2)
        self.root = Node(id='1')
        self.insert(node=self.root, depth=0,
                    depth_leaf=depth_leaf, id=1, user_list=users)
        self.set_label()
        return self.root
