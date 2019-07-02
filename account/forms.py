# accounts.forms.py
from django import forms

from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = User.objects.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError("phone is taken")
        return phone

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class LoginForm(forms.ModelForm):
        password = forms.CharField(widget=forms.PasswordInput)
        class Meta:
            model = User
            fields = ('phone','password',)

        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            qs = User.objects.filter(phone=phone)
            if not qs.exists():
                raise forms.ValidationError("phone number doesnt exists")
            return phone

        def clean_password(self):
            # Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            return password1
