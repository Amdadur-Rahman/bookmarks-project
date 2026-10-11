from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model




class UserRegistrasionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('password dont match')
        return cleaned_data

    

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PsswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
            widget=forms.PasswordInput
        )
    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('this password is not carrect')
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('password dont match')
        return cleaned_data

    def save(self, commit= True):
        new_password = self.cleaned_data.get('new_password')
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user


class PsswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email):
            raise forms.ValidationError ('email not found')
        return email

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError ('password dont match')
        return cleaned_data

