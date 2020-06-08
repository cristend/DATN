'''
input:
# n number of user: each user denote by u.
# r number of revoke user: each revoke user denote u_r, otherwise denote u_v.
output:
# List of subset different cover all valid user u_v.
# Generate LABEL following collection of cover.
# Generate secret infomation for each u_v following collection of cover.
# Encrypt and decrypt
support function:
# RPF
'''
# main
import pdb
import math


class User():
    def __init__(self, id):
        self.id = id
        self.si = None
        self.key = None
        self.status = True


class Users():
    def __init__(self):
        self.users = None

    def create_user(self, users):
        user_list = list()
        for user in range(users):
            new_user = User(id=(user+1)*10)
            user_list.append(new_user)
        self.users = user_list
        return None

    def print(self):
        for user in self.users:
            print(f'user_id: {user.id}')


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

    def find_lca(self, node1_id, node2_id, root):
        print(f'node1: {node1_id}, node2: {node2_id}')
        ancestor = self.lca(node1_id=node1_id, node2_id=node2_id, root=root)
        return ancestor[0]

    def lca(self, node1_id, node2_id, root):
        if root is None:
            return None
        self.count += 1
        print(f'{self.count} and {root.id}')
        if root.id == node1_id or root.id == node2_id:
            return root
        left_lca = self.lca(
            node1_id=node1_id, node2_id=node2_id, root=root.left)
        if isinstance(left_lca, tuple):
            if left_lca[1] is True:
                return left_lca[0], True
        right_lca = self.lca(
            node1_id=node1_id, node2_id=node2_id, root=root.right)
        if left_lca and right_lca:
            return root, True

        return left_lca if left_lca is not None else right_lca

    def leaf_count(self, root):
        if root is None:
            return 0, None
        if is_leaf(root):
            return 1, root

        left_leafs = self.leaf_count(root=root.left)
        count = (left_leafs[0], left_leafs[1])
        right_leafs = self.leaf_count(root=root.right)
        if right_leafs[1] is None:
            count = (count[0]+right_leafs[0], count[1])
        else:
            count = (count[0]+right_leafs[0], right_leafs[1])

        return count

    def get_parent(self, ancestor, node):
        if ancestor.left.id == node.id or ancestor.right.id == node.id:
            return ancestor
        if ancestor.left:
            left_child = self.get_parent(
                ancestor=ancestor.left, node=node)
            if left_child:
                return left_child
        if ancestor.right:
            right_child = self.get_parent(
                ancestor=ancestor.right, node=node)
            if right_child:
                return right_child
        return None

    def is_descendant(self, ancestor, node):
        if ancestor is None:
            return None
        if ancestor.id == node.id:
            return True
        left_child = self.is_descendant(ancestor=ancestor.left, node=node)
        if left_child:
            return True
        right_child = self.is_descendant(ancestor=ancestor.right, node=node)
        if right_child:
            return True
        return None

    def get_subset(self, node1, node2, ancestor):
        subsets = set()
        parent1 = ancestor.left if self.is_descendant(
            ancestor=ancestor, node=node1) else ancestor.right
        parent2 = ancestor.left if parent1.id == ancestor.right\
            else ancestor.right
        if parent1.id != node1.id:
            subset = Subset(ancestor=parent1, descendant=node1)
            subsets.add(subset)
        if parent2.id != node2.id:
            subset = Subset(ancestor=parent2, descendant=node2)
            subsets.add(subset)
        # print(f'subset:{subsets}--node1:{node1.id}--node2:{node2.id}')
        return subsets

    def count_lca(self, root):
        if self.leaf_count(root) == 0:
            return set(), 0, root
        left_leafs, left_leaf = self.leaf_count(root.left)
        right_leafs, right_leaf = self.leaf_count(root.right)
        left_subset = right_subset = set()
        if left_leafs > 1:
            left_subset, left_leafs, left_leaf = self.count_lca(root=root.left)
        if right_leafs > 1:
            right_subset, right_leafs, right_leaf = self.count_lca(
                root=root.right)
        if left_leafs == 1 and right_leafs == 1:
            subsets = self.get_subset(
                node1=left_leaf, node2=right_leaf, ancestor=root)
            root.left = None
            root.right = None
            subsets.update(left_subset)
            subsets.update(right_subset)
            return subsets, 1, root

    def print_tree(self, node=None):
        node = self.root if node is None else node
        print(node.id, end=' ')
        if node.left is not None:
            self.print_tree(node.left)
        if node.right is not None:
            self.print_tree(node.right)
        if node == self.root:
            print('')


class Steiner_tree():
    def __init__(self, tree):
        self.st = tree.root

    def build(self, revokes, root=None):
        root = self.st if root is None else root
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

    def print_st(self, root):
        if is_leaf(root):
            print(root)
            return None
        if root.left:
            self.print_st(root=root.left)
        if root.right:
            self.print_st(root=root.right)
        print(root)


class Subset():
    def __init__(self, ancestor, descendant):
        self.nodes = None
        self.ancestor = ancestor
        self.descendant = descendant

    def __repr__(self):
        return f'S({self.ancestor.id},{self.descendant.id})'


def is_power(num, base):
    if base in {0, 1}:
        return num == base
    power = int(math.log(num, base) + 0.5)
    return base ** power == num


def is_leaf(node):
    if node.left is None and node.right is None:
        return True


users = Users()
users.create_user(8)
users.print()
test = Binary_tree(7)
test.build(user_list=users)
test.print_tree()
revokes = [10, 50, 60, 30, 70]
st = Steiner_tree(test)
st_tree = st.build(revokes)
# pdb.set_trace()
# st.print_st(root=st_tree)
# count = test.leaf_count(test.root.left)
# pdb.set_trace()
# count = test.leaf_count(root=st_tree)
# ar = test.is_descendant(ancestor=test.root.left,
#                         node=test.root.right.left.left)
subset = test.count_lca(root=st_tree)[0]
# subset = test.get_subset(test.root.left.left.left, test.root.left.right.left, test.root.left)
pdb.set_trace()
