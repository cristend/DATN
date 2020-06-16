import math


def node_count(root, count=0):
    if root is None:
        return None
    count += 1
    if root.left:
        count += node_count(root=root.left)
    if root.right:
        count += node_count(root=root.right)
    return count


def get_nodes(root):
    if root is None:
        return []
    left_list, right_list = [], []
    nodes = list()
    if root.left:
        left_list = get_nodes(root=root.left)
    if root.right:
        right_list = get_nodes(root=root.right)
    nodes.append(root)
    nodes.extend(left_list)
    nodes.extend(right_list)
    return nodes


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


def bit_str_xor(left, right):
    len_left = len(left)
    len_right = len(right)
    index = abs(len_left-len_right)
    if len_left > len_right:
        left_bit, right_bit = left[:index], left[index:]
        if isinstance(left, bytes) and isinstance(right, bytes):
            xor_bit = bytes([_left ^ _right for _left,
                             _right in zip(right_bit, right)])
        else:
            xor_bit = ''.join([str(int(_left) ^ int(_right))
                               for _left, _right in zip(right_bit, right)])
        result = (left_bit + xor_bit)
    elif len_left < len_right:
        left_bit, right_bit = right[:index], right[index:]
        if isinstance(left, bytes) and isinstance(right, bytes):
            xor_bit = bytes([_left ^ _right for _left,
                             _right in zip(right_bit, left)])
        else:
            xor_bit = ''.join([str(int(_left) ^ int(_right))
                               for _left, _right in zip(right_bit, left)])
        result = (left_bit + xor_bit)
    else:
        if isinstance(left, bytes) and isinstance(right, bytes):
            result = bytes([_left ^ _right for _left,
                            _right in zip(left, right)])
            count = 1
            for byte in result:
                if byte == 0:
                    result = result[1:]
                    count += 1
                    continue
                break
        else:
            result = (''.join([str(int(_left) ^ int(_right))
                               for _left, _right in zip(
                                   right, left)]).lstrip('0'))
            pad = (-len(result)) % 8 + len(result)
            result = result.zfill(pad)
    return result


def to_str(_str):
    return ''.join(
        [chr(int(_str[i:i+8], 2)) for i in range(0, len(_str), 8)])


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
