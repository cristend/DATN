import math
from broadcast.server.node import Node
from broadcast.utils.common import is_power, is_leaf


class Binary_tree():
    def __init__(self, users_number):
        self.root = None
        self.build(users_number=users_number)

    def insert(self, node, depth, depth_leaf, id):
        if depth == depth_leaf-1:
            node.left = Node(id=2*id)
            node.right = Node(id=2*id+1)
            return None
        if node.left is None:
            left_id = 2*id
            node.left = Node(id=left_id)
            self.insert(node=node.left, depth=depth+1,
                        depth_leaf=depth_leaf, id=left_id)
        if node.right is None:
            right_id = 2*id + 1
            node.right = Node(id=right_id)
            self.insert(node=node.right, depth=depth+1,
                        depth_leaf=depth_leaf, id=right_id)
        return None

    def build(self, users_number):
        leafs = None
        depth_leaf = None
        if is_power(users_number, 2):
            depth_leaf = math.log(users_number, 2)
        else:
            leafs = 2**(int(math.log(users_number, 2)) + 1)
            depth_leaf = math.log(leafs, 2)
        self.root = Node(id=1)
        self.insert(node=self.root, depth=0,
                    depth_leaf=depth_leaf, id=1)
        return self.root

    def get_ST(self, revokes, root=None):
        root = self.root if root is None else root
        if is_leaf(root):
            if root.id in revokes:
                leaf = Node(id=root.id)
                return leaf
            return None
        new_root = Node(id=root.id)
        if root.left:
            left_child = self.get_ST(revokes=revokes, root=root.left)
            if left_child:
                new_root.left = left_child
                left_child.parent = new_root
        if root.right:
            right_child = self.get_ST(
                revokes=revokes, root=root.right)
            if right_child:
                new_root.right = right_child
                right_child.parent = new_root
        if new_root.left or new_root.right:
            return new_root
