from django.forms import BooleanField, ModelForm, DateTimeField, DateTimeInput

from mailings.models import Client, Message, Mailings


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class ClientForm(StyleMixin, ModelForm):
    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'surname',
            'email',
            'comment'
        )


class MessageForm(StyleMixin, ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'text')


class MailingsForm(StyleMixin, ModelForm):
    date_time = DateTimeField(
        widget=DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            ),
        label='Время первой рассылки',
        required=True,
    )
    class Meta:
        model = Mailings
        fields = (
            'message',
            'clients',
            'period',
            'date_time',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['clients'].queryset = Client.objects.filter(creator=user)
            self.fields['message'].queryset = Message.objects.filter(creator=user)


class MailingModeratorForm(StyleMixin, ModelForm):
    """Класс форма для редактирования рассылки модератором"""
    class Meta:
        model = Mailings
        fields = ('status',)

