class Node():
    def __init__(self, id, data=None, label=None):
        self.id = id
        self.left = None
        self.right = None
        self.parent = None
        self.data = data
        self.label = label

    def __repr__(self):
        left_child = self.left.id if self.left else None
        right_child = self.right.id if self.right else None
        parent = self.parent.id if self.parent else None
        status = 'user' if self.data else 'node'
        if self.id == 1:
            status = 'root'
        node = ('id: {}, left_child: {},'
                ' right_child: {}, parent: {}, status: {}, label: {}').format(
            self.id, left_child, right_child, parent, status, self.label)
        return node
