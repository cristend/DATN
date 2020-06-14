class Subset():
    def __init__(self, ancestor, descendant):
        self.ancestor = ancestor
        self.descendant = descendant

    def __repr__(self):
        return f'S({self.ancestor.id},{self.descendant.id})'
