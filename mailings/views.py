from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.utils.datetime_safe import datetime
from blog.models import Blog
from config.settings import ZONE
from mailings.forms import MailingsForm, ClientForm, MessageForm, MailingModeratorForm
from mailings.models import Mailings, Client, Message, MailingAttempt


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Добавление клиента
    """
    template_name = 'clients/clients_form.html'
    model = Client
    form_class = ClientForm
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy("mailings:clients_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user  # Задаем creator перед сохранением
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Изменение данных о клиенте
    """
    template_name = 'clients/clients_form.html'
    login_url = reverse_lazy('users:login')
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailings:clients_list")


class ClientListView(ListView):
    """
    Отображение списка клиентов
    """
    template_name = 'clients/clients_list.html'
    model = Client



class ClientDetailView(DetailView):
    """
    Отображение клиента
    """
    template_name = 'clients/clients_detail.html'
    model = Client



class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление клиента
    """
    model = Client
    template_name = 'clients/clients_confirm_delete.html'
    success_url = reverse_lazy("mailings:clients_list")


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Добавление сообщения
    """
    model = Message
    form_class = MessageForm
    template_name = 'message/message_form.html'
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user  # Задаем creator перед сохранением
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Изменение сообщения
    """
    login_url = reverse_lazy('users:login')
    model = Message
    form_class = MessageForm
    template_name = 'message/message_form.html'
    success_url = reverse_lazy("mailings:message_list")


class MessageListView(ListView):
    """
    Отображение списка сообщений
    """
    model = Message
    template_name = 'message/message_list.html'



class MessageDetailView(DetailView):
    """
    Отображение сообщения
    """
    model = Message
    template_name = 'message/message_detail.html'



class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление сообщения
    """
    login_url = reverse_lazy('users:login')
    model = Message
    template_name = 'message/message_confirm_delete.html'
    success_url = reverse_lazy("mailings:message_list")



class MailingsCreateView(LoginRequiredMixin, CreateView):
    """
    Добавление рассылки
    """
    login_url = reverse_lazy('users:login')
    model = Mailings
    form_class = MailingsForm
    success_url = reverse_lazy("mailings:mailings_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class MailingsUpdateView(LoginRequiredMixin, UpdateView):
    """
    Изменение рассылки
    """
    model = Mailings
    form_class = MailingsForm
    success_url = reverse_lazy("mailings:mailings_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.creator:
            return MailingsForm
        if user.has_perm('mailings.can_disable_mailings') and user.has_perm('mailings.can_view_any_mailings'):
            return MailingModeratorForm


class MailingsListView(ListView):
    """
    Отображение списка рассылок
    """
    model = Mailings


class MailingsDetailView(DetailView):
    """
    Отображение рассылки
    """
    model = Mailings

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['error_at'] = MailingAttempt.objects.filter(mailing=self.object)
        if self.object.status == 'created' or self.object.status == 'closed':
            data['run_send'] = 'start'
        elif self.object.status == 'active':
            data['run_send'] = 'stop'
        else:
            data['run_send'] = None
        return data

class MailingsDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление рассылки
    """
    model = Mailings
    success_url = reverse_lazy("mailings:mailings_list")



class HomePageView(LoginRequiredMixin, TemplateView):
    """
    Отображение главной страницы
    """
    template_name = "base.html"
    login_url = reverse_lazy('users:login')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Рассылки"
        mailings = Mailings.objects.filter(creator=self.request.user).count()
        context["mailings"] = mailings
        active_mailings = Mailings.objects.filter(status='active', creator=self.request.user).count()
        context["active_mailings"] = active_mailings
        unique_clients = Client.objects.filter(creator=self.request.user).count()
        context["unique_clients"] = unique_clients
        context["random_Blog"] = Blog.objects.order_by("?")[:3]
        return context


class MailingAttemptListView(LoginRequiredMixin, ListView):
    """
    Отображение списка отчетов рассылки
    """
    model = MailingAttempt
    paginate_by = 30

    def get_queryset(self):
        mailing_id = self.kwargs.get('mailings_id')
        mailing = get_object_or_404(Mailings, pk=mailing_id)
        data = MailingAttempt.objects.filter(newsletter=mailing).order_by('-date_time')
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        mailing_id = self.kwargs.get('mailing_id')
        mailing = get_object_or_404(Mailings, pk=mailing_id)
        data['mailing'] = mailing
        return data


def start_sending(request, mailing_id):
    """
    Запуск рассылки
    """
    mailing = get_object_or_404(Mailings, pk=mailing_id)
    if mailing.status == 'created' and mailing.date_time < datetime.now(ZONE):
        return redirect(reverse('mailings:datetime_late', args=[mailing_id]))
    mailing.status = 'active'
    mailing.save()
    return redirect(reverse('mailings:mailings_view', args=[mailing_id]))


def stop_sending(request, mailing_id):
    """
    Остановка рассылки
    """
    mailing = get_object_or_404(Mailings, pk=mailing_id)
    mailing.status = 'closed'
    mailing.save()
    return redirect(reverse('mailings:mailings_view', args=[mailing_id]))

class DatetimeLateTemplateView(TemplateView):
    """
    Предупреждение о том что дата первой отправки рассылки - просрочена
    """
    template_name = 'mailings/datetime_late.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['mailing_id'] = self.kwargs.get('mailing_id')
        return data
