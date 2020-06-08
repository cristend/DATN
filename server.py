import math
from resource import is_leaf, is_power, is_descendant, leaf_count


class Node():
    def __init__(self, id, data=None):
        self.id = id
        self.left = None
        self.right = None
        self.data = data

    def __repr__(self):
        left_child = True if self.left else False
        right_child = True if self.right else False
        status = 'user' if self.data else 'non-user'
        node = ('id: {}, left_child: {},'
                ' right_child: {}, status: {}').format(
            self.id, left_child, right_child, status)
        return node


class Binary_tree():
    def __init__(self, users):
        self.root = None
        self.users = users
        self.revokes = 0
        self.count = 0

    def insert(self, node, depth, depth_leaf, id, user_list):
        if depth == depth_leaf-1:
            left_user = user_list.users.pop(0)
            right_user = user_list.users.pop(0)
            node.left = Node(id=left_user.id, data=left_user)
            node.right = Node(id=right_user.id, data=right_user)
            return None
        if node.left is None:
            left_id = 2*id
            node.left = Node(id=left_id)
            self.insert(node=node.left, depth=depth+1,
                        depth_leaf=depth_leaf, id=left_id, user_list=user_list)
        if node.right is None:
            right_id = 2*id + 1
            node.right = Node(id=right_id)
            self.insert(node=node.right, depth=depth+1,
                        depth_leaf=depth_leaf, id=right_id,
                        user_list=user_list)
        return None

    def build(self, user_list):
        # number of leaf in tree, should be a factor of 2.
        leafs = None
        # number of leaf padding if n is not a factor of 2
        pad_leafs = None
        # depth of a leaf
        DEPTH_LEAF = None
        # number of users, also as leafs if users is a factor of 2.
        users = self.users
        # number of revoke users.
        revokes = self.revokes
        if is_power(users, 2):
            DEPTH_LEAF = math.log(users, 2)
        else:
            leafs = 2**(int(math.log(users, 2)) + 1)
            pad_leafs = leafs - users
            revokes += pad_leafs
            DEPTH_LEAF = math.log(leafs, 2)
        self.root = Node(id=1)
        self.insert(node=self.root, depth=0,
                    depth_leaf=DEPTH_LEAF, id=1, user_list=user_list)

    # def find_lca(self, node1_id, node2_id, root):
    #     print(f'node1: {node1_id}, node2: {node2_id}')
    #     ancestor = self.lca(node1_id=node1_id, node2_id=node2_id, root=root)
    #     return ancestor[0]

    # def lca(self, node1_id, node2_id, root):
    #     if root is None:
    #         return None
    #     self.count += 1
    #     print(f'{self.count} and {root.id}')
    #     if root.id == node1_id or root.id == node2_id:
    #         return root
    #     left_lca = self.lca(
    #         node1_id=node1_id, node2_id=node2_id, root=root.left)
    #     if isinstance(left_lca, tuple):
    #         if left_lca[1] is True:
    #             return left_lca[0], True
    #     right_lca = self.lca(
    #         node1_id=node1_id, node2_id=node2_id, root=root.right)
    #     if left_lca and right_lca:
    #         return root, True

    #     return left_lca if left_lca is not None else right_lca

    # def get_parent(self, ancestor, node):
    #     if ancestor.left.id == node.id or ancestor.right.id == node.id:
    #         return ancestor
    #     if ancestor.left:
    #         left_child = self.get_parent(
    #             ancestor=ancestor.left, node=node)
    #         if left_child:
    #             return left_child
    #     if ancestor.right:
    #         right_child = self.get_parent(
    #             ancestor=ancestor.right, node=node)
    #         if right_child:
    #             return right_child
    #     return None

    def get_subset(self, node1, node2, ancestor):
        subsets = set()
        parent1 = ancestor.left if is_descendant(
            ancestor=ancestor, node=node1) else ancestor.right
        parent2 = ancestor.left if parent1.id == ancestor.right\
            else ancestor.right
        if parent1.id != node1.id:
            subset = Subset(ancestor=parent1, descendant=node1)
            subsets.add(subset)
        if parent2.id != node2.id:
            subset = Subset(ancestor=parent2, descendant=node2)
            subsets.add(subset)
        return subsets

    def find_subsets(self, root):
        if leaf_count(root) == 0:
            return set(), 0, root
        left_leafs, left_leaf = leaf_count(root.left)
        right_leafs, right_leaf = leaf_count(root.right)
        left_subset = right_subset = set()
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
            subsets.update(left_subset)
            subsets.update(right_subset)
            return subsets, 1, root


class Steiner_tree():
    def __init__(self, tree):
        self.root = tree.root

    def build(self, revokes, root=None):
        root = self.root if root is None else root
        if is_leaf(root):
            if root.data.id in revokes:
                leaf = Node(id=root.id, data=root.data)
                return leaf
            return None
        new_root = Node(id=root.id, data=root.data)
        if root.left:
            left_child = self.build(revokes=revokes, root=root.left)
            if left_child:
                new_root.left = left_child
        if root.right:
            right_child = self.build(revokes=revokes, root=root.right)
            if right_child:
                new_root.right = right_child
        if new_root.left or new_root.right:
            return new_root
        return None


class Subset():
    def __init__(self, ancestor, descendant):
        self.nodes = None
        self.ancestor = ancestor
        self.descendant = descendant

    def __repr__(self):
        return f'S({self.ancestor.id},{self.descendant.id})'
