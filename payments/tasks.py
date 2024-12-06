from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from dues.models import Dues

from .models import Payment
from .sms_client import send_sms_get


User = get_user_model()




@shared_task
def send_payment_notification(user_id, amount, month):
    user = User.objects.get(id=user_id)
    message = f"Hello {user.first_name.capitalize()}, your payment of GHS {amount} for {month} has been successfully processed."
    send_sms_get([user.phone_number], message)


@shared_task
def send_monthly_reminders():
    users = User.objects.all()
    for user in users:
        message = "This is a reminder to pay your monthly dues."
        send_sms_get([user.phone_number], message)
        send_mail(
            "Monthly Dues Reminder", message, settings.DEFAULT_FROM_EMAIL, [user.email]
        )


@shared_task
def send_unpaid_dues_reminders():
    today = datetime.today()
    dues = Dues.objects.filter(month__lt=today)
    for due in dues:
        unpaid_users = User.objects.exclude(
            payment__dues=due, payment__is_verified=True
        )
        for user in unpaid_users:
            message = (
                f"Reminder: You have unpaid dues for {due.month.strftime('%B %Y')}."
            )
            send_sms_get([user.phone_number], message)
            send_mail(
                "Unpaid Dues Reminder",
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
