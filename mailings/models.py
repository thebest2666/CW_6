from django.db import models

from users.models import User


class Client(models.Model):
    """
    Информация о клиенте
    """

    email = models.EmailField(max_length=200, verbose_name="Почта клиента", unique=True)
    first_name = models.CharField(max_length=200, verbose_name="Имя клиента")
    last_name = models.CharField(max_length=200, verbose_name="Фамилия клиента")
    surname = models.CharField(
        max_length=200, verbose_name="Отчество клиента", null=True, blank=True
    )
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата добавления клиента")
    creator = models.ForeignKey(
        User, verbose_name="Создатель", on_delete=models.CASCADE,
    )

    def __str__(self):
        surname = f" {self.surname}" if self.surname else ""
        return f"{self.first_name} {self.last_name}{surname}: {self.email}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Mailings(models.Model):
    """
    Настройка рассылки
    """

    STATUS_CHOICES = [
        ("created", "Рассылка создана"),
        ("active", "Рассылка запущена"),
        ("closed", "Рассылка завершена"),
    ]
    PERIOD_CHOICES = [
        ("days", "Ежедневная рассылка"),
        ("weeks", "Еженедельная рассылка"),
        ("months", "Ежемесячная рассылка"),
    ]
    clients = models.ManyToManyField(
        Client,
        verbose_name="Клиенты",
        related_name='clients'
    )
    date_time = models.DateTimeField(
        verbose_name="Дата и время отправки первой рассылки"
    )
    period = models.CharField(
        verbose_name="Периодичность рассылки", choices=PERIOD_CHOICES
    )
    status = models.CharField(
        verbose_name="Статус рассылки", choices=STATUS_CHOICES, default="created"
    )
    created_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата создания рассылки"
    )
    creator = models.ForeignKey(
        User, verbose_name="Создатель", on_delete=models.CASCADE,
    )
    message = models.ForeignKey(
        "Message",
        on_delete=models.SET_NULL,
        verbose_name="Сообщение",
        blank=True,
        null=True,
    )


    def __str__(self):
        return f"Рассылка #{self.pk}: {self.date_time} ({self.created_at})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ('can_disable_mailings', 'can disable mailings'),
            ('can_view_any_mailings', 'can view any mailings lists')
        ]



class Message(models.Model):
    """
    Сообщение для рассылки
    """

    title = models.CharField(max_length=200, verbose_name="Заголовок сообщения")
    text = models.TextField(verbose_name="Текст сообщения")
    creator = models.ForeignKey(
        User, verbose_name="Создатель", on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class MailingAttempt(models.Model):
    """
    Информация о попытках рассылки
    """

    mailing = models.ForeignKey(
        Mailings,
        on_delete=models.SET_NULL,
        verbose_name="Рассылка",
        blank=True,
        null=True,
        related_name="mailing",
    )
    date_time = models.DateTimeField(verbose_name="Дата и время попытки рассылки")
    successful_attempt = models.BooleanField(verbose_name="Попытка успешная")
    error_at = models.CharField(
        max_length=255,
        verbose_name="Отчет в случае ошибки попытки",
        null=True,
        blank=True,
    )
    next_send = models.DateTimeField(
        verbose_name="Дата и время следующей попытки рассылки", null=True, blank=True
    )

    def __str__(self):
        return f"Попытка #{self.pk}: {self.date_time} (рассылка # {self.mailing.pk}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
