from django.db import models


class Blog(models.Model):
    """
    Информация о блоге
    """
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок",
    )
    description = models.TextField(
        verbose_name="Содержимое",
    )
    photo = models.ImageField(
        upload_to="blog/photo",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    created_at = models.DateField(
        auto_now=True,
        blank=True,
        null=True,
    )
    views_counter = models.IntegerField(
        verbose_name="Количество просмотров",
        default=0,
    )
    is_published = models.BooleanField(
        verbose_name="Признак публикации",
        default=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
