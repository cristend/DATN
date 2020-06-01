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
            new_user = User(id=user)
            user_list.append(new_user)
        self.users = user_list
        return None

    def print(self):
        for user in self.users:
            print(user.id)


class Node():
    def __init__(self, id, data=None):
        self.id = id
        self.left = None
        self.right = None
        self.data = data


class Binary_tree():
    def __init__(self, users):
        self.root = None
        self.users = users
        self.revokes = 0

    def insert(self, node, depth, depth_leaf, id, user_list):
        if depth == depth_leaf-1:
            left_user = user_list.users.pop()
            right_user = user_list.users.pop()
            node.left = Node(id=(2*id), data=left_user)
            node.right = Node(id=(2*id+1), data=right_user)
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

    def sub_tree(self, root, node):
        if root is node:
            pass

    def print_tree(self, node=None):
        node = self.root if node is None else node
        print(node.id, end=' ')
        if node.left is not None:
            self.print_tree(node.left)
        if node.right is not None:
            self.print_tree(node.right)


# class Steiner_tree():
#     def __init__(self):
#         self.st = list()

#     def path(self, node, revokes):
#         if node.left is None:
#             if node.data.status is False:
#                 self.st.append(node)
#                 pass
#             return None
#         if node.left is not None:
#             self.path(node.left)
#         if node.right is not None:
#             self.path(node.right)


class Subset():
    def __init__(self, users, revokes):
        self.users = users
        self.revokes = revokes

    def build_tree(self):
        pass


def is_power(num, base):
    if base in {0, 1}:
        return num == base
    power = int(math.log(num, base) + 0.5)
    return base ** power == num


users = Users()
users.create_user(8)
test = Binary_tree(7)
test.build(user_list=users)
test.print_tree()
