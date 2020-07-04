from app.api import bp


@bp.route('/users/<int:id>', methods={'GET'})
def get_infor(id):
    if(id):
        return {'a': 'etc', 'b': 'mnb'}
    pass
