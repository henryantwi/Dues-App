from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset.html"
    email_template_name = "account/password_reset_email.html"
    html_email_template_name = "account/password_reset_email.html"


urlpatterns = [
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("webmaster/", admin.site.urls),
    path("account/", include("account.urls")),
    path("", include("dues.urls")),
    path("payments/", include("payments.urls")),
    # Password reset
    path("reset_password/", CustomPasswordResetView.as_view(), name="reset_password"),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
