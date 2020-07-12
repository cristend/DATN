import os
from Crypto import Random
from app.models import Labels, License, Media, User
from app.broadcast.server import bt


def create_table_labels(db):
    Labels.query.delete()
    users_number = int(os.environ.get('NUMBER_OF_USER'))
    n_labels = 2*users_number
    for i in range(n_labels):
        labeli = str(list(Random.new().read(32)))
        label = Labels(label=labeli)
        db.session.add(label)
    db.session.commit()


def create_table_licenses(db):
    License.query.delete()
    user_id_list = bt.users_list
    for user_id in user_id_list:
        _licence = License(license_id=user_id)
        db.session.add(_licence)
    users = User.query.all()
    for user in users:
        user.license_id = None
    db.session.commit()


def create_table_media(db):
    Media.query.delete()
    db.session.commit()
