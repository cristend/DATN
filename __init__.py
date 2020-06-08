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
from server import Binary_tree, Steiner_tree, Subset
from users import User, Users
from resource import print_tree

users = Users()
users.create_user(8)
users.print()
test = Binary_tree(7)
test.build(user_list=users)
print_tree(node=test.root)
revokes = [10, 50, 60, 30, 70]
st = Steiner_tree(test)
st_tree = st.build(revokes)
# pdb.set_trace()
print_tree(node=st_tree)
# count = test.leaf_count(test.root.left)
# pdb.set_trace()
# count = test.leaf_count(root=st_tree)
# ar = test.is_descendant(ancestor=test.root.left,
#                         node=test.root.right.left.left)
# subset = test.count_lca(root=st_tree)[0]
# subset = test.get_subset(test.root.left.left.left, test.root.left.right.left,
#  test.root.left)
# G = PRNG(10011001)
# a = format(random.getrandbits(128), 'b')
# print(a)

pdb.set_trace()
