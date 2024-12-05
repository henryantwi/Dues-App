import secrets
import uuid

from django.conf import settings
from django.db import models

from dues.models import Dues

from .paystack import Paystack


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dues = models.ForeignKey(Dues, on_delete=models.RESTRICT, related_name="payments")

    payment_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    ref = models.CharField(max_length=255)
    transaction_id = models.CharField(
        max_length=255, blank=True, null=True
    )

    def verify_payment(self) -> bool:
        paystack = Paystack()
        formatted_total_paid = self.get_formatted_amount()
        try:
            status, result, id = paystack.verify_payment(self.ref, formatted_total_paid)
            if status and result["amount"] == formatted_total_paid:
                self.is_verified = True
                self.transaction_id = id
                self.save()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error verifying payment: {e}")
            return False

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def get_formatted_amount(self):
        return int(float(self.dues.amount) * 100)

    def __str__(self):
        return f"{self.user.first_name} - {self.is_verified} on {self.payment_date.strftime('%Y-%m-%d %H:%M:%S')}"
