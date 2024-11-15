from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from mailings.forms import StyleMixin
from users.models import User


class UserRegisterForm(StyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")



class UserProfileChangeForm(StyleMixin, UserChangeForm):
    """
    Редактирование своего профиля
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserModeratorForm(StyleMixin, ModelForm):
    """
    Отображения всех пользователей
    """
    class Meta:
        model = User
        fields = ('is_active',)