from src.common.resource import is_leaf
from src.server.node import Node


class Steiner_tree():
    def __init__(self, root):
        self.root = root

    def build(self, revokes, root=None):
        root = self.root if root is None else root
        if is_leaf(root):
            if root.data.id in revokes:
                leaf = Node(id=root.id, data=root.data, label=root.label)
                return leaf
            return None
        new_root = Node(id=root.id, data=root.data, label=root.label)
        if root.left:
            left_child = self.build(revokes=revokes, root=root.left)
            if left_child:
                new_root.left = left_child
                left_child.parent = new_root
        if root.right:
            right_child = self.build(
                revokes=revokes, root=root.right)
            if right_child:
                new_root.right = right_child
                right_child.parent = new_root
        if new_root.left or new_root.right:
            return new_root
