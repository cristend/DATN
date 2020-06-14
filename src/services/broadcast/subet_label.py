from src.crypto.ggm import G_M
from src.services.broadcast.label import Label


class SubsetLabel():
    def __init__(self, subsets, bt):
        self.subsets = subsets
        self.label = Label(bt=bt)

    def get_key(self):
        subset_keys = dict()
        for subset in self.subsets:
            labelij = self.label.get_labelij(
                nodei=subset.ancestor, nodej=subset.descendant)
            ll_key = G_M(X=labelij)
            ll_key_key = f'{subset.ancestor.id}{subset.descendant.id}'
            subset_keys[ll_key_key] = ll_key
        return subset_keys
