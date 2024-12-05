from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"  # Specifies that the ForeignKey in Profile is to 'user'


class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
    model = CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )

    readonly_fields = ["date_joined"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "other_name", "phone_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )

    inlines = [ProfileInline]


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "notification_type",
        "notification_changes_made_to_account",
        "notification_any_news",
    )
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = (
        "notification_type",
        "notification_changes_made_to_account",
        "notification_any_news",
    )


# Register CustomUser with the admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Register Profile separately
admin.site.register(Profile, ProfileAdmin)
