import os
import ast
from app.models import Labels
from .binary_tree import Binary_tree

NUMBER_OF_USER = int(os.environ.get('NUMBER_OF_USER'))


bt = Binary_tree(NUMBER_OF_USER)
label_records = Labels.query.all()
labels = dict()
for label_record in label_records:
    label = bytes(ast.literal_eval(label_record.label))
    labels[label_record.id-1] = bytes(label)
