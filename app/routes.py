import os
import json
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask import render_template, flash, redirect, \
    url_for, request, send_file
from app import app, db
from app.utils.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, License, Media
from app.utils.email import send_email
from app.broadcast.server.functions import get_user_labels
from app.broadcast.server import labels
from app.broadcast.server.packet import create_packet


@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.group == 1:
        return redirect(url_for('admin'))
    media = Media.query.all()
    return render_template('index.html', title='Home Page', media=media)


@app.route('/admin')
@login_required
def admin():
    media = Media.query.all()
    return render_template('admin.html', media=media)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if user.group == 1:
            return redirect(url_for('admin'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# @app.route('/add_admin')
# def add_admin():
#     user = User(username='admin', email='nguyenvanthu1905@gmail.com',
#                 group=1, status=True)
#     user.set_password('admin')
#     db.session.add(user)
#     db.session.commit()
#     return


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    _license = None
    if user.license_id:
        _license = License.query.filter_by(
            license_id=user.license_id).first_or_404()
    return render_template('user.html', user=user, _license=_license)


@app.route('/admin/broadcast')
@login_required
def broadcast():
    msg = request.args.get('msg', None)
    return render_template('broadcast.html', msg=msg)


@app.route('/uploader', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if not f.filename:
            return redirect(url_for('broadcast'))
        file_name = os.path.join(app.root_path,
                                 app.config['UPLOAD_FOLDER'],
                                 secure_filename(f.filename))
        f.save(file_name)
        licenses = License.query.filter_by(assigned=False).all()
        revokes = [_license.license_id for _license in licenses]
        licenses = License.query.filter_by(revoked=True).all()
        revoked = [_license.license_id for _license in licenses]
        revokes.extend(revoked)
        import pdb; pdb.set_trace()
        packet = ''
        with open(file_name, 'rb') as _file:
            data = _file.read()
            packet = create_packet(revokes=revokes, data=data)
            _file.close()
        name, extension = file_name.split('.')
        with open(name + '.enc.' + extension, 'w') as _file:
            _file.write(packet)
            _file.close()
        os.remove(file_name)
        name = name.split('/').pop() + '.enc.' + extension
        detail = f.filename.split('.').pop(0)
        media = Media(name=name, detail=detail)
        db.session.add(media)
        db.session.commit()
        return redirect(url_for('broadcast', msg='file uploaded successfully'))


@app.route('/admin/delete/<media_id>')
def delete_content(media_id):
    media = Media.query.filter_by(id=media_id).first()
    db.session.delete(media)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/active')
@login_required
def active():
    subject = 'Welcome to our service!'
    sender = os.environ.get('SYSTEM_EMAIL')
    recipients = [current_user.email]
    text_body = 'Here is your secret information and decryption tool attach with it. Thank you for using our service!'  # noqa
    html_body = ''
    license_records = License.query.filter_by(assigned=False).all()
    license_list = [record.license_id for record in license_records]
    license_id = license_list.pop(0)
    labels_dict = get_user_labels(user_id=license_id, labels=labels)
    data = json.dumps(labels_dict)
    # send_email(subject=subject, sender=sender, recipients=recipients,
    #            text_body=text_body, html_body=html_body, data=data)
    with open(f'secret_{current_user.username}.json', 'w') as f:
        f.write(data)
        f.close()
    user = User.query.filter_by(
        username=current_user.username).first_or_404()
    _licence = License.query.filter_by(
        license_id=license_id
    ).first()
    if user:
        _licence.assigned = True
        user.status = True
        user.license_id = license_id
        db.session.commit()
    else:
        raise(Exception)
    return redirect(url_for('user', username=current_user.username))


@app.route('/download/<file_name>')
def download(file_name):
    uploads = os.path.join(app.root_path,
                           app.config['UPLOAD_FOLDER'], file_name)
    return send_file(uploads, as_attachment=True)


@app.route('/admin/license')
def license():
    # licenses = License.query.filter_by(assigned=True).all()
    users = User.query.join(License, User.license_id == License.license_id)\
        .add_columns(License.assigned, License.revoked)\
        .filter_by(assigned=True)\
        .all()
    data = list()
    for user in users:
        header = user[0].license_id
        infor = [user[0].username, user[0].email]
        revoke = user[2]
        _data = [header, infor, revoke]
        data.append(_data)

    return render_template('license.html', data=data)


@app.route('/admin/revoke/<license_id>')
def revoke(license_id):
    _license = License.query.filter_by(license_id=license_id).first_or_404()
    _license.revoked = True
    db.session.commit()
    return redirect(url_for('license'))
