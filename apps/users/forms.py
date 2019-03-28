from django import forms
from .models import UserProfile

class LoginForm(forms.Form):
    account = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)


class RegisterForm(forms.Form):
    account = forms.CharField(required=True, min_length=5)
    password = forms.CharField(required=True, min_length=8)
    confirm_password = forms.CharField(required=True, min_length=8)

    def clean(self):
        account = self.cleaned_data.get('account')
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('confirm_password')
        user_profile = UserProfile.objects.filter(username=account)
        if user_profile:
            raise forms.ValidationError('账号已存在，请输入新的账号')
        if pwd1 == pwd2:
            pass
        else:
            raise forms.ValidationError("两次密码输入不一致")