from calendar import month_name
from datetime import date

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from payments.models import Payment

from .models import Dues


@login_required
def index(request):
    return render(request, "payments/index.html")

@login_required
def dues_list(request, year=None):
    payment_status = request.GET.get("payment_status")
    user_payments = Payment.objects.filter(user=request.user, is_verified=True)
    paid_dues_ids = user_payments.values_list("dues_id", flat=True)

    # Get the current date
    today = date.today()
    current_year = year if year else today.year

    # Filter dues to show only months <= current month of the current year
    dues = Dues.objects.filter(month__year=current_year)

    # Sort dues by month
    dues = sorted(
        dues,
        key=lambda due: list(month_name).index(due.month.strftime("%B")),
        reverse=True,
    )

    dues_status = []
    for due in dues:
        is_paid = due.id in paid_dues_ids
        dues_status.append(
            {
                "due": due,
                "is_paid": is_paid,
                "payment": user_payments.filter(dues=due).first() if is_paid else None,
            }
        )

    # Pagination
    paginator = Paginator(dues_status, 6)  # Show 10 dues per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "dues_status": page_obj,
        "payment_status": payment_status,
        "current_year": current_year,
        "page_obj": page_obj,
        "today": today,
    }
    return render(request, "payments/list.html", context)
