import os
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.utils.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.utils.email import send_email


@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.group == 1:
        redirect(url_for('admin'))
    return render_template('index.html', title='Home Page')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


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
#                 group=1, status=False)
#     user.set_password('admin')
#     db.session.add(user)
#     db.session.commit()
#     return


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/admin/upload')
@login_required
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if not f.filename:
            return redirect(url_for('upload'))
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return 'file uploaded successfully'


@app.route('/active')
@login_required
def active():
    subject = 'Welcome to our service!'
    sender = 'nguyenvanthu1905@gmail.com'
    recipients = ['twenking001@gmail.com']
    text_body = 'Here is your secret information and decryption tool attach with it. Thank you for using our service!'  # noqa
    html_body = ''
    send_email(subject, sender, recipients, text_body, html_body)
    user = User.query.filter_by(
        username=current_user.username).first_or_404()
    if user:
        user.status = True
        db.session.commit()
    else:
        raise(Exception)
    return redirect(url_for('user', username=current_user.username))
