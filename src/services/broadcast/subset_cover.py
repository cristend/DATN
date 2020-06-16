from src.server.subset import Subset
from src.common.resource import is_descendant, leaf_count


class SubsetCover():
    def __init__(self, bt, st):
        self.bt = bt
        self.st = st

    def get_subset(self, node1, node2, ancestor):
        subsets = []
        parent1 = ancestor.left if is_descendant(
            ancestor=ancestor, node=node1) else ancestor.right
        parent2 = ancestor.left if parent1.id == ancestor.right\
            else ancestor.right
        if parent1.id != node1.id:
            subset = Subset(ancestor=parent1, descendant=node1)
            subsets.append(subset)
        if parent2.id != node2.id:
            subset = Subset(ancestor=parent2, descendant=node2)
            subsets.append(subset)
        return subsets

    def find_subsets(self, root=None):
        root = self.st if root is None else root
        if leaf_count(root) == 0:
            return [], 0, root
        left_leafs, left_leaf = leaf_count(root.left)
        right_leafs, right_leaf = leaf_count(root.right)
        left_subset = right_subset = []
        if left_leafs > 1:
            left_subset, left_leafs, left_leaf = self.find_subsets(
                root=root.left)
        if right_leafs > 1:
            right_subset, right_leafs, right_leaf = self.find_subsets(
                root=root.right)
        if left_leafs == 1 and right_leafs == 1:
            subsets = self.get_subset(
                node1=left_leaf, node2=right_leaf, ancestor=root)
            root.left = None
            root.right = None
            subsets.extend(left_subset)
            subsets.extend(right_subset)
            return subsets, 1, root
        left_subset.extend(right_subset)
        subsets = left_subset
        leafs = left_leafs + right_leafs
        root = right_leaf if right_leafs == 1 else left_leaf
        return subsets, leafs, root

    def _find_subsets(self):
        result = self.find_subsets()
        subsets, number, root = result
        return subsets
