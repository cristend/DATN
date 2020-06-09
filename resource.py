import math


def leaf_count(root):
    if root is None:
        return 0, None
    if is_leaf(root):
        return 1, root

    left_leafs = leaf_count(root=root.left)
    count = (left_leafs[0], left_leafs[1])
    right_leafs = leaf_count(root=root.right)
    if right_leafs[1] is None:
        count = (count[0]+right_leafs[0], count[1])
    else:
        count = (count[0]+right_leafs[0], right_leafs[1])

    return count


def is_power(num, base):
    if base in {0, 1}:
        return num == base
    power = int(math.log(num, base) + 0.5)
    return base ** power == num


def is_leaf(node):
    if node.left is None and node.right is None:
        return True


def is_descendant(ancestor, node):
    if ancestor is None:
        return None
    if ancestor.id == node.id:
        return True
    left_child = is_descendant(ancestor=ancestor.left, node=node)
    if left_child:
        return True
    right_child = is_descendant(ancestor=ancestor.right, node=node)
    if right_child:
        return True
    return None


def print_tree(node, flag=True, inline=False):
    if inline:
        print(node, end=' ')
    else:
        print(node)
    if node.left is not None:
        print_tree(node.left, flag=False)
    if node.right is not None:
        print_tree(node.right, flag=False)
    if flag:
        print('')
