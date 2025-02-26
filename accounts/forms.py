from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


'''ログイン用フォーム'''
class LoginForm(AuthenticationForm):
    class Meta:
      model = User


class CreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
