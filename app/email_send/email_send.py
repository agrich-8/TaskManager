import os
import smtplib, ssl
from email.mime.text import MIMEText


def send_email1(email, username, code):
    port = 587  # For starttls
    smtp_server = "smtp.yandex.ru"
    sender_email = os.environ.get('MAIL_USERNAME')
    receiver_email = email
    password = os.environ.get('MAIL_PASSWORD')
    message = f"""\
    <p>Dear {username},</p>
    <p>Password change confirmation code<p>
    <p>{code}<p>
    <p><small>Note: replies to this email address are not monitored.</small></p>"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        msg = MIMEText(message, 'html')
        server.sendmail(sender_email, receiver_email, msg.as_string())


def send_email2(email: str | None, username, code):
    port = 587  # For starttls
    smtp_server = "smtp.yandex.ru"
    sender_email = os.environ.get('MAIL_USERNAME')
    receiver_email = email
    password = os.environ.get('MAIL_PASSWORD')
    message = f"""\
    <p>Dear {username},</p>
    <p>Password change confirmation code<p>
    <p>{code}<p>
    <p><small>Note: replies to this email address are not monitored.</small></p>"""
    server = smtplib.SMTP(smtp_server, port)
    try:
        server.login(sender_email, password)
        msg = MIMEText(message, 'html')
        server.sendmail(sender_email, receiver_email, msg.as_string())
    
    except:
        print('Error')
