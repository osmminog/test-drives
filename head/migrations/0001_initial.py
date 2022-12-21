# Generated by Django 3.1.1 on 2020-12-27 16:54

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название бренда')),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='images/brands/', verbose_name='Логотип бренда')),
            ],
            options={
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Модель авто')),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('available', models.BooleanField(default=True, verbose_name='Показывать')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='head.brand', verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='CarVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления видео на сайт')),
                ('date_realise', models.IntegerField(verbose_name='Выход видео (Число дней, месяцев, лет...назад)')),
                ('text_date_realise', models.CharField(max_length=250, verbose_name='Подпись к выходу видео (дней, месяцев, лет...назад)')),
                ('age', models.IntegerField(verbose_name='Сколько дней назад вышло видео')),
                ('title_video', models.CharField(max_length=250, verbose_name='Заголовок видео')),
                ('id_videos', models.CharField(max_length=250, verbose_name='ID видео')),
                ('number_of_views', models.IntegerField(verbose_name='Количество просмотров, тыс.')),
                ('image_urls', models.URLField(verbose_name='Ссылка на обложку видео')),
                ('image_jpg', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Обложка видео jpg')),
                ('image_webp', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Обложка видео webp')),
                ('image_webp_small', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Small Обложка видео webp')),
                ('url', models.URLField(verbose_name='Ссылка на видео')),
                ('hq', models.CharField(max_length=250, verbose_name='Размер картинки')),
                ('available', models.BooleanField(default=True, verbose_name='Показывать')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carvideos', to='head.brand', verbose_name='Марка авто')),
                ('car', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='brand', chained_model_field='brand', on_delete=django.db.models.deletion.CASCADE, show_all=True, to='head.car', verbose_name='Модель авто')),
            ],
            options={
                'ordering': ['brand'],
            },
        ),
    ]
