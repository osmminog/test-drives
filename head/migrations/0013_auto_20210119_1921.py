# Generated by Django 3.1.1 on 2021-01-19 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0012_auto_20210119_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='history',
            field=models.TextField(blank=True),
        ),
    ]
