import base64
import os
import math
from Crypto import Random
from ..utils.crypto.ggm import G_L, G_M, G_R
from ..server.subset import Subset
from ..utils.common import leaf_count, bit_str_xor
from ..utils.crypto.EL import ElCipher
from ..utils.crypto.aes import AESCTR


def get_labels(users_number):
    n_labels = 2*users_number-1
    labels = dict()
    for i in range(n_labels):
        label_i = Random.new().read(32)
        labels[i+1] = label_i
    return labels


def get_subset(left_leaf, right_leaf, ancestor):
    subsets = []
    left_child = ancestor.left
    right_child = ancestor.right
    if left_child != left_leaf:
        subset = Subset(ancestor=left_child.id, descendant=left_leaf.id)
        subsets.append(subset)
    if right_child != right_leaf:
        subset = Subset(ancestor=right_child.id, descendant=right_leaf.id)
        subsets.append(subset)
    return subsets


def get_subset_leaf(node_id):
    parent_id = int(node_id/2) if node_id % 2 == 0 else int((node_id-1)/2)
    subset = Subset(ancestor=parent_id, descendant=node_id)
    return [subset]


def find_subsets(root):
    if leaf_count(root) == 0:
        return [], 0, root
    left_leafs, left_leaf = leaf_count(root.left)
    right_leafs, right_leaf = leaf_count(root.right)
    left_subset = right_subset = []
    if left_leafs > 1:
        left_subset, left_leafs, left_leaf = find_subsets(
            root=root.left)
    if right_leafs > 1:
        right_subset, right_leafs, right_leaf = find_subsets(
            root=root.right)
    if left_leafs == 1 and right_leafs == 1:
        subsets = get_subset(
            left_leaf=left_leaf, right_leaf=right_leaf, ancestor=root)
        root.left = None
        root.right = None
        subsets.extend(left_subset)
        subsets.extend(right_subset)
        return subsets, 1, root
    left_subset.extend(right_subset)
    subsets = left_subset
    leafs = left_leafs + right_leafs
    if root.id == 1:
        if left_leafs:
            subset = Subset(ancestor=root.id, descendant=left_leaf.id)
            subsets.append(subset)
        else:
            subset = Subset(ancestor=root.id, descendant=right_leaf.id)
            subsets.append(subset)
    else:
        root = right_leaf if right_leafs == 1 else left_leaf
    return subsets, leafs, root


def _find_subsets(root):
    if root is None:
        return []
    left_leafs, left_leaf = leaf_count(root.left)
    right_leafs, right_leaf = leaf_count(root.right)
    NUMBER_OF_USER = int(os.environ.get('NUMBER_OF_USER'))
    if left_leafs+right_leafs == 1:
        single_node = left_leaf if left_leafs == 1 else right_leaf
        subset = Subset(ancestor=root.id, descendant=single_node.id)
        return [subset]
    total_leafs = left_leafs+right_leafs
    half_leafs = int(NUMBER_OF_USER/2)
    if total_leafs == NUMBER_OF_USER:
        return None
    if total_leafs == half_leafs and left_leafs == half_leafs:
        subset = Subset(ancestor=root.id, descendant=root.left.id)
        return [subset]
    if total_leafs == half_leafs and right_leafs == half_leafs:
        subset = Subset(ancestor=root.id, descendant=root.right.id)
        return [subset]
    result = find_subsets(root=root)
    subsets, number, root = result
    return subsets

# --- end find subsets ---
# --- find labels ---


def get_labelij(root, leaf, labels):
    current_index = leaf
    path = dict()
    while True:
        current_index, direction = get_node_in_path(current_index)
        path[current_index] = direction
        if current_index == root:
            break
    list_node_id = list(path.keys())
    current_index = list_node_id.pop()
    label = labels[current_index]
    while True:
        label = G_R(label) if path[current_index] else G_L(label)
        if not list_node_id:
            break
        current_index = list_node_id.pop()
    return label


def get_key(subsets, labels):
    subset_keys = dict()
    for subset in subsets:
        labelij = get_labelij(root=subset.ancestor,
                              leaf=subset.descendant, labels=labels)
        ll_key = G_M(X=labelij)
        ll_key_key = str(subset.ancestor) + '-' + str(subset.descendant)
        subset_keys[ll_key_key] = ll_key
    return subset_keys


def get_user_labels(user_id, labels):
    # find the path from root to u:
    if not labels[user_id]:
        raise Exception('Invalid index of labels')
    path = dict()
    user_id = user_id
    parent_id = user_id
    while True:
        parent_id, direction = get_node_in_path(parent_id)
        path[parent_id] = direction
        if parent_id == 1:
            break
    # With path compute all label
    labels_dict = dict()
    list_node_id = list(path.keys())
    while list_node_id:
        current_index = list_node_id.pop()
        i_index = current_index
        j_index = i_index
        label = labels[i_index]
        while True:
            label_left = G_L(label)
            label_right = G_R(label)
            if path[j_index]:
                j_index = j_index*2
                ij = str(i_index) + '-' + str(j_index)
                label = label_right
                labels_dict[ij] = list(label_left)
                j_index = j_index + 1
            else:
                j_index = j_index*2+1
                ij = str(i_index) + '-' + str(j_index)
                label = label_left
                labels_dict[ij] = list(label_right)
                j_index = j_index - 1
            if j_index == user_id:
                break
    labels_dict['0-0'] = list(labels[0])
    return labels_dict


def get_node_in_path(u):
    return (int(u/2), 0) if (u % 2 == 0) else (int((u-1)/2), 1)
# unpack


def find_id(subset_ids, labels):
    user_subset_ids = list(labels.keys())
    # last user label can compute user id information
    user_last_subset_id = user_subset_ids[-2]
    # find user_id
    user_id = get_user_id(subset_id=user_last_subset_id)
    # find subset contain user
    user_subset_id = find_subset(u_id=user_id, subset_ids=subset_ids)
    if not user_subset_id:
        return None
    # find user subset contain key
    root_id, leaf_id = [int(x) for x in user_subset_id.split('-')]
    key_subset_id = None
    for subset in user_subset_ids:
        high, low = [int(x) for x in subset.split('-')]
        if high != root_id:
            continue
        depth_leaf = int(math.log(leaf_id, 2))
        depth_low = int(math.log(low, 2))
        if depth_low <= depth_leaf:
            bound_left = bound_right = low
            for multi in range(depth_leaf-depth_low):
                bound_left *= 2
                bound_right = bound_right*2 + 1
            if bound_left <= leaf_id and leaf_id <= bound_right:
                key_subset_id = subset
    return [key_subset_id, user_subset_id]


def find_subset(u_id, subset_ids):
    NUMBER_OF_USER = int(os.environ.get('NUMBER_OF_USER'))
    depth = int(math.log(NUMBER_OF_USER, 2))
    for subset_id in subset_ids:
        if subset_id == '0-0':
            continue
        high, low = [int(x) for x in subset_id.split('-')]
        high_bound_left = high_bound_right = high
        low_bound_left = low_bound_right = low
        high_depth = depth - int(math.log(high, 2))
        low_depth = depth - int(math.log(low, 2))
        for multi in range(high_depth):
            high_bound_left *= 2
            high_bound_right = high_bound_right*2 + 1
        for multi in range(low_depth):
            low_bound_left *= 2
            low_bound_right = low_bound_right*2 + 1
        if (high_bound_left <= u_id and u_id < low_bound_left)\
                or (u_id > low_bound_right and u_id <= high_bound_right):
            return subset_id


def get_user_id(subset_id):
    left, right = [int(x) for x in subset_id.split('-')]
    user_id = left*2 if left*2 != right else left*2 + 1
    return user_id


def mapping(subset_ids, ciphers):
    _map = dict()
    for id, cipher in zip(subset_ids, ciphers):
        _map[id] = cipher
    return _map


def unpack(packet, user_labels):
    header, body = packet.split('[')[1].split(']')
    header = header.split(',')
    body = body.strip(',')
    split_index = int(len(header)/2)
    subset_ids, U, ciphers = (
        header[:split_index],
        header[split_index:split_index+1].pop(),
        header[split_index+1:])
    cipher_dict = mapping(subset_ids=subset_ids, ciphers=ciphers)
    if subset_ids[0] == 'none':
        return None
    if '0-0' in subset_ids:
        subset_label = bytes(user_labels['0-0'])
        user_subset_id = '0-0'
    else:
        ids = find_id(subset_ids=subset_ids, labels=user_labels)
        if not ids:
            return None
        key_subset_id, user_subset_id = ids
        if not key_subset_id:
            return None
        root, leaf = [int(x) for x in user_subset_id.split('-')]
        if key_subset_id == user_subset_id:
            subset_label = bytes(user_labels[key_subset_id])
        else:
            labels = {root: bytes(user_labels[key_subset_id])}
            subset_label = get_labelij(root=root, leaf=leaf, labels=labels)
    ll_key = G_M(subset_label)
    U = base64.b64decode(U.encode())
    el = ElCipher()
    raw = bit_str_xor(left=U, right=user_subset_id.encode())
    K = el.decrypt(key=ll_key, raw=raw,
                   cipher_text=cipher_dict[user_subset_id])
    fk = AESCTR(key=K)
    msg = fk.decrypt(enc=body).decode()
    return msg
