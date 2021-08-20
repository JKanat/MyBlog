from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status


def send_activation_code(email, activation_code, status):
    if status == 'register':
        context = {
            'text_detail': "Thank you for registration!",
            "email": email,
            "domain": "http://localhost:8000",
            "activation_code": activation_code
         }
        msg_html = render_to_string('email.html', context)
        message = strip_tags(msg_html)
        send_mail(
            'Activate Your Account',
            message,
            'stackoveerflow_admin@gmail.com',
            [email, ],
            html_message=msg_html,
            fail_silently=False
    )
    elif status == 'reset_password':
        send_mail(
            'Reset Your Account',
            f'Код активации: {activation_code}',
            'stackoveerflow_admin@gmail.com',
            [email, ],
            fail_silently=False,
        )
