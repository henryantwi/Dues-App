import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Dues(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dues"
        verbose_name_plural = "Dues"

    def __str__(self) -> str:
        return f"{self.amount} for {self.month.strftime('%B')}, {self.month.year}"

    def clean(self) -> None:
        # Extract the year and month from the month field
        year = self.month.year
        month = self.month.month

        # Check if there's already a Dues entry for the same year and month
        if Dues.objects.filter(month__year=year, month__month=month).exists():
            raise ValidationError(
                _("Dues for %(month)s, %(year)s already exists."),
                params={"month": self.month.strftime("%B"), "year": year},
            )

    def save(self, *args, **kwargs) -> None:
        # Call the clean method to perform the validation
        self.clean()
        super().save(*args, **kwargs)
