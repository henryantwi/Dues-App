from django import forms

from .models import CustomUser, Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone_number"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "required": True}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.startswith("233"):
            raise forms.ValidationError(
                "Phone number must start with the country code '233'."
            )
        return phone_number


class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_image",
            "about",
            "address",
            "notification_changes_made_to_account",
            "notification_any_news",
            "notification_type",
        ]
        widgets = {
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "notification_type": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "role": forms.Select(attrs={"class": "form-control"}),
            "notification_changes_made_to_account": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "notification_any_news": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
