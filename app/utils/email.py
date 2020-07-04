from flask_mail import Message
from app import mail


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    with open('media/test.txt', 'rb') as f:
        data = f.read()
        msg.attach(
            'decrypt.py',
            'application/octect-stream',
            data)
    mail.send(msg)