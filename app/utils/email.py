from flask_mail import Message
from app import mail
from app import app
import os


def send_email(subject, sender, recipients, text_body, html_body, data=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if data:
        msg.attach(
            'secret.json',
            'application/octect-stream',
            data)
    # filename = os.path.join(app.root_path,
    #                         'static',
    #                         'decrypt')
    # with open(filename, 'rb') as f:
    #     msg.attach(
    #         'decrypt',
    #         'application/octect-stream',
    #         f.read())
    mail.send(msg)
