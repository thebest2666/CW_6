import secrets
import string
import random

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView

from users.forms import UserRegisterForm, UserProfileChangeForm, UserModeratorForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    """
    Создание пользователя
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Верификация пользователя
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def reset_password(request):
    """
    Сброс пароля
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        check = User.objects.filter(email=email).exists()
        if check:
            user = User.objects.get(email=email)
            letters = string.ascii_letters
            digits = string.digits
            special_chars = string.punctuation
            all_chars = letters + digits + special_chars
            password = ''.join(random.choice(all_chars) for _ in range(8))
            user.set_password(password)
            user.save()
            send_mail(
                subject="Сброс пароля",
                message=f"Пароль сброшен. Ваш новый ременный пароль: {password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return render(request, 'users/success_reset_password.html')
        else:
            return render(request, 'users/error_reset_password.html')
    return render(request, 'users/reset_password.html')


class UserListView(UserModeratorForm, PermissionRequiredMixin, ListView):
    """
    Отображение всех пользователей
    """
    model = User
    template_name = 'user_list.html'
    permission_required = 'users.can_view_list_of_users'



class ProfileUpdateView(UpdateView):
    """
    Редактирования своего профиля
    """
    model = User
    form_class = UserProfileChangeForm
    success_url = reverse_lazy('mailings:base')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['pk'])


    def get_form_class(self):
        user = self.request.user
        if user.pk == self.object.pk:
            return UserProfileChangeForm
        if user.has_perm('users.block_users'):
            return UserModeratorForm
        raise PermissionDenied