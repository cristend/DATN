from Crypto import Random
from broadcast.utils.crypto.ggm import G_L, G_M, G_R
from broadcast.server.subset import Subset
from broadcast.utils.common import leaf_count


def get_labels(users_number):
    n_labels = 2*users_number-1
    labels = dict()
    for i in range(n_labels):
        label_i = Random.new().read(32)
        labels[i+1] = label_i
    return labels


def get_key(subsets, labels):
    subset_keys = dict()
    for subset in subsets:
        labelij = get_labelij(nodei=subset.ancestor,
                              nodej=subset.descendant, labels=labels)
        ll_key = G_M(X=labelij)
        ll_key_key = str(subset.ancestor.id) + str(subset.descendant.id)
        subset_keys[ll_key_key] = ll_key
    return subset_keys


#
# ---find subset functions---

def get_subset(left_leaf, right_leaf, ancestor):
    subsets = []
    left_child = ancestor.left
    right_child = ancestor.right
    if left_child != left_leaf:
        subset = Subset(ancestor=left_child, descendant=left_leaf)
        subsets.append(subset)
    if right_child != right_leaf:
        subset = Subset(ancestor=right_child, descendant=right_leaf)
        subsets.append(subset)
    return subsets


def find_subsets(root):
    if leaf_count(root) == 0:
        return [], 0, root
    left_leafs, left_leaf = leaf_count(root.left)
    right_leafs, right_leaf = leaf_count(root.right)
    if left_leafs+right_leafs == 1:
        return left_leaf if left_leaf else right_leaf
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
    root = right_leaf if right_leafs == 1 else left_leaf
    return subsets, leafs, root


def _find_subsets(root):
    result = find_subsets(root=root)
    subsets, number, root = result
    return subsets


# --- end find subsets ---
# --- find labels ---


def get_labelij(nodei, nodej, labels):
    root = nodei.id
    leaf = nodej.id
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


def get_user_labels(user, root, labels):
    # find the path from root to u:
    path = dict()
    user_id = user.id
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
        label = labels[i_index]
        while True:
            label_left = G_L(label)
            label_right = G_R(label)
            if path[i_index]:
                j_index = i_index*2
                ij = str(i_index)+str(j_index)
                label = label_right
                labels[ij] = label_left
            else:
                j_index = i_index*2+1
                ij = str(i_index)+str(j_index)
                label = label_left
                labels[ij] = label_right
            if j_index == user_id:
                break
    return labels_dict


def get_node_in_path(u):
    return (int(u/2), 0) if (u % 2 == 0) else (int((u-1)/2), 1)
