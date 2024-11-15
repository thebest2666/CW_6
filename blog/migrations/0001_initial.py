# Generated by Django 4.2.2 on 2024-11-10 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Содержимое')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='blog/photo', verbose_name='Изображение')),
                ('created_at', models.DateField(auto_now=True, null=True)),
                ('views_counter', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('is_published', models.BooleanField(default=True, verbose_name='Признак публикации')),
            ],
            options={
                'verbose_name': 'блог',
                'verbose_name_plural': 'блоги',
            },
        ),
    ]