from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token

User = get_user_model()


@shared_task
def send_verification_email(user_id, domain):
    user = User.objects.get(id=user_id)
    subject = "Activate your Account"
    message = render_to_string(
        "account/account_activation_email.html",
        {
            "user": user,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


