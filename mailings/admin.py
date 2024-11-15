from django.contrib import admin
from mailings.models import Mailings, MailingAttempt, Client, Message

admin.site.register(Client)
admin.site.register(Mailings)
admin.site.register(MailingAttempt)
admin.site.register(Message)