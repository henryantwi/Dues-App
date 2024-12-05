from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str = None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True  # Make sure new users are active
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields):
        """
        Create and return a superuser with email, password, and superuser privileges.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)  # Make sure the superuser is active

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of a username.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    other_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(
        max_length=30, blank=False
    )
    is_active = models.BooleanField(default=True)  # Set to True for active users by default
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No required fields, as `email` is used as the username

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def get_full_name(self) -> str:
        """
        Returns the user's full name by combining the first and last names.
        """
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def __str__(self):
        return self.get_full_name()


class Profile(models.Model):
    """
    A user profile model to store additional information about users.
    """
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile"
    )
    profile_image = models.ImageField(upload_to="profile_pics", default="default.jpg")
    about = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=225, null=True, blank=True)
    role = models.CharField(default="Member", max_length=25)

    # Notification settings
    notification_changes_made_to_account = models.BooleanField(default=False)
    notification_any_news = models.BooleanField(default=False)
    notification_type = models.CharField(
        max_length=10,
        choices=[
            ("sms", "SMS"),
            ("email", "Email"),
            ("none", "None"),
        ],
        default="email",
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "Users Profile"

    def __str__(self) -> str:
        return f"{self.user.first_name.capitalize()}'s Profile"
