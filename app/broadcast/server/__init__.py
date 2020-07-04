import os
from .binary_tree import Binary_tree
from .functions import get_labels

# NUMBER_OF_USER = os.environ.get('NUMBER_OF_USER')
NUMBER_OF_USER = 8
labels = get_labels(NUMBER_OF_USER)


bt = Binary_tree(NUMBER_OF_USER)
labels = get_labels(NUMBER_OF_USER)
