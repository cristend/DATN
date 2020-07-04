class Node():
    def __init__(self, id, data=None, label=None):
        self.id = id
        self.left = None
        self.right = None

    def __repr__(self):
        left_child = self.left.id if self.left else None
        right_child = self.right.id if self.right else None
        node = ('id: {}, left_child: {}, right_child: {}').format(
            self.id, left_child, right_child)
        return node
