# Generated by Django 3.1.1 on 2020-12-28 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0002_auto_20201228_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carvideo',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='Дата добавления видео на сайт'),
        ),
    ]
