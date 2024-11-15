from django.urls import path

from mailings.apps import MailingsConfig

from mailings.views import MailingsListView, MailingsCreateView, ClientCreateView, MailingsDetailView, \
    MailingsUpdateView, MailingsDeleteView, ClientDetailView, ClientUpdateView, ClientDeleteView, MessageListView, \
    MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, ClientListView, HomePageView, \
    start_sending, stop_sending

app_name = MailingsConfig.name

urlpatterns = [
    path("", HomePageView.as_view(), name="base"),

    path("mailings/", MailingsListView.as_view(), name="mailings_list"),
    path("mailings/create/", MailingsCreateView.as_view(), name="mailings_create"),
    path("mailings/view/<int:pk>", MailingsDetailView.as_view(), name="mailings_view"),
    path("mailings/edit/<int:pk>", MailingsUpdateView.as_view(), name="mailings_edit"),
    path("mailings/delete/<int:pk>", MailingsDeleteView.as_view(), name="mailings_delete"),

    path("clients/", ClientListView.as_view(), name="clients_list"),
    path("clients/create/", ClientCreateView.as_view(), name="clients_create"),
    path("clients/view/<int:pk>", ClientDetailView.as_view(), name="clients_view"),
    path("clients/edit/<int:pk>", ClientUpdateView.as_view(), name="clients_edit"),
    path("clients/delete/<int:pk>", ClientDeleteView.as_view(), name="clients_delete"),

    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/view/<int:pk>", MessageDetailView.as_view(), name="message_view"),
    path("message/edit/<int:pk>", MessageUpdateView.as_view(), name="message_edit"),
    path("message/delete/<int:pk>", MessageDeleteView.as_view(), name="message_delete"),

    path('mailings/<int:mailing_id>/start_sending', start_sending, name='start_sending'),
    path('mailings/<int:mailing_id>/stop_sending', stop_sending, name='stop_sending'),
]
