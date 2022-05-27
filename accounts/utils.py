import os
from email.mime .text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.mail import send_mail
from django.conf import settings

email= os.environ.get('EMAIL_HOST_USER')
password = os.environ.get('EMAIL_HOST_PASSWORD')

class Util:
    @staticmethod
    # helps to use this class method without instantiating the class itself
    def send_email(data,fail_silently = False):
        subject=data['email_subject']
        body = data['email_body']
        # to_emails argument is always a list of emails and not a string or any data type
        to = data['to_email']
        # assert will check and raise an error if the to_email argument is not a list
        assert isinstance(to, list)
        msg = MIMEMultipart('alternative')
        txt_part = MIMEText(body, 'plain')
        msg.attach(txt_part)
        html_part = MIMEText(body)
        msg.attach(html_part)
        msg_str = msg.as_string()
        send_mail(subject,body,'rajishmaharjan123@gmail.com',to,fail_silently=False,)


