from app import app, db
from app.models import User
from app.utils.tables import create_table_labels, create_table_licenses  # noqa

# create_table_labels(db)
# create_table_licenses(db)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
