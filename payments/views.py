from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from dues.models import Dues

from .models import Payment
from .sms_client import send_sms_get


@login_required
def make_payment(request, uuid):
    dues = get_object_or_404(Dues, pk=uuid)
    existing_payment = Payment.objects.filter(
        user=request.user, dues=dues, is_verified=True
    ).first()
    if existing_payment:
        # Redirect or show a message indicating the payment is already completed
        return render(
            request, "payments/payment_already_done.html", {"payments": existing_payment}
        )

    payment = Payment.objects.create(user=request.user, dues=dues)
    payment.save()
    amount = int(float(dues.amount) * 100)
    user_email = request.user.email

    context = {
        "dues": dues,
        "payment": payment,
        "amount": amount,
        "user_email": user_email,
        "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY,
    }

    return render(request, "payments/make_payment.html", context)


@login_required
def verify_payment(request, ref):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        sms = send_sms_get(
            [request.user.phone_number],
            f"Hello {request.user.first_name.capitalize()}, your payment of GHS {payment.dues.amount} for {payment.dues.month.strftime('%B')} has been successfully processed.",
        )
        return redirect(f"{reverse('dues:dues_list')}?payment_status=success")
    else:
        sms = send_sms_get(
            [request.user.phone_number],
            f"Hello {request.user.first_name.capitalize()}, there was an error processing your payment. Please contact the Treasurer at support@madrasutannaasuhiyya.com.",
        )
        return redirect(f"{reverse('dues:dues_list')}?payment_status=failure")
