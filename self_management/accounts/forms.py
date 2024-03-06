from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


'''ログイン用フォーム'''
class LoginForm(AuthenticationForm):

    # bootstrap4対応
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class CreateForm(UserCreationForm):
    email = forms.EmailField(
        max_length = 255,
     )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
