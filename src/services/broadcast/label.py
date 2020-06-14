from src.crypto.ggm import G_R, G_L


class Label():
    def __init__(self, bt):
        self.bt = bt

    def get_labelij(self, nodei, nodej):
        label = None
        child = nodej
        path = dict()
        while True:
            current_node = child
            child = child.parent
            left_or_right = '0' if current_node == child.left else '1'
            path[child.id] = left_or_right
            if child == nodei:
                break
        current_node = nodei
        label = nodei.label
        while True:
            left_or_right = int(path[current_node.id])
            if left_or_right:
                current_node = current_node.right
                label = G_R(label)
            else:
                current_node = current_node.left
                label = G_L(label)
            if current_node == nodej:
                break
        return label

    def get_hangoff_labelij(self, leaf, nodei, path):
        # Function compute all label Sij with i is index of nodei and j are
        # All node hang-off the path from user to root
        # Dictionary store label, each element have key is Sij and value
        # is LABELij
        labels = dict()
        # Index_node is instant of current node that sit in the path from user
        # to root in the loop
        index_node = nodei
        # Label is temporary label compute by previous node'label
        label = nodei.label
        # I_index is instant for i
        i_index = nodei.id
        # While block iterating over all node that sit in path from
        # user to root
        while True:
            # Left or right mean that previous child is left or right child
            # of current node, which need to chose which GGM should use.
            left_or_right = int(path[index_node.id])
            label_left = G_L(label)
            label_right = G_R(label)
            if left_or_right:
                j_index = index_node.left.id
                index_node = index_node.right
                label = label_left
                label_key = f'{i_index}{j_index}'
            else:
                j_index = index_node.right.id
                index_node = index_node.left
                label = label_right
                label_key = f'{i_index}{j_index}'
            # Store label with index
            labels[label_key] = label
            if index_node == leaf:
                break
            label = label_right if left_or_right else label_left
        return labels

    def get_user_labels(self, leaf, root=None):
        # Function collect all labelij which store in each user
        root = self.bt.root if root is None else root
        # List of node that lie on the path from user to root (except user).
        node_list = list()
        # Dictionary of all label in collection, each element have key is Sij
        # and value is label.
        labels = dict()
        # Dictionary of all node sit in the path from user to root, each
        # element have key is direction of previous node and value is a node
        # that is parant of previous node
        path = dict()
        parent = leaf
        # Assign value to node_list and path
        while True:
            # Iteration from leaf to root
            child = parent
            parent = parent.parent
            # '0' mean child is left-child of parent, '1' mean right-child
            path_value = '0' if parent.left == child else '1'
            path[parent.id] = path_value
            node_list.append(parent)
            if parent == root:
                # Reset temporary variable to reuse
                parent = leaf
                break
        # For block iterating over all node sit in the path from user to root
        # Each iterator compute all label available from that node
        for node in node_list:
            label_dict = self.get_labelij(leaf=leaf, nodei=node, path=path)
            labels = {**labels, **label_dict}
        return labels
