from django.contrib.auth import password_validation
from store.models import Address, Category, Product
from django import forms
import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _

# Creéation des formulaires


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mot de pass",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "mot de passe"}
        ),
    )
    password2 = forms.CharField(
        label="Confirmez votre mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "confirmez votre mot de passe",
            }
        ),
    )
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "adresse Email"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {"email": "Email"}
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "nom d 'utilisateur"}
            )
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["locality", "city", "state"]
        widgets = {
            "locality": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "montext"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ville"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Pays"}
            ),
        }


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "auto-focus": True,
                "class": "form-control",
                "placeholder": "Current Password",
            }
        ),
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "New Password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        ),
    )


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": "form-control"}
        ),
    )


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ("update_at", "created_at")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("update_at", "created_at")
