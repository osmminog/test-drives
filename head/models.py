from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey
from PIL import Image
from taggit.managers import TaggableManager


class Brand(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название бренда')
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/brands/', blank=True, verbose_name='Логотип бренда')
    history = models.TextField(blank=True)
    
    class Meta:
        ordering = ('title',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
       return reverse('head:video_list_by_brand', args=[self.slug])


class Car(models.Model):
    title = models.CharField(max_length=250, verbose_name='Модель авто')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars', verbose_name='Бренд')
    slug = models.SlugField(max_length=250,unique=True)
    available = models.BooleanField(default=True, verbose_name='Показывать')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
       return reverse('head:video_list_by_car', args=[self.brand.slug, self.slug])


class CarVideo(models.Model):
    created = models.DateField(auto_now_add=True, verbose_name='Дата добавления видео на сайт')
    age = models.DateField(verbose_name='Дата выхода видео')
    title_video = models.CharField(max_length=250, verbose_name='Заголовок видео')
    id_videos = models.CharField(max_length=250, verbose_name='ID видео')
    number_of_views = models.IntegerField(verbose_name='Количество просмотров')
    image_urls = models.URLField(verbose_name='Ссылка на обложку видео')
    image_jpg = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Обложка видео jpg')
    image_webp = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Обложка видео webp')
    image_webp_small = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Small Обложка видео webp')
    url = models.URLField(verbose_name='Ссылка на видео')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='carvideos', verbose_name='Марка авто')
    car = ChainedForeignKey(Car, chained_field="brand", chained_model_field="brand", show_all=False, auto_choose=True, sort=True, verbose_name='Модель авто')
    hq = models.CharField(max_length=250, verbose_name='Размер картинки')
    available = models.BooleanField(default=True, verbose_name='Показывать')
    
    class Meta:
        ordering = ['brand']
        verbose_name = 'video'
        verbose_name_plural = 'videos'

    def __str__(self):
        return self.title_video

    def get_absolute_url(self):
       return reverse('head:carvideo_feed', args=[self.brand.slug, self.slug])


class PublishedManager(models.Manager): 
    def get_queryset(self): 
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = ( 
        ('draft', 'Draft'), 
        ('published', 'Published'), 
    ) 
    title = models.CharField(max_length=250) 
    description = models.CharField(max_length=500, default='', verbose_name='Описание статьи') 
    slug = models.SlugField(max_length=250, unique_for_date='publish') 
    body = models.TextField() 
    publish = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации") 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    image_jpg = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Обложка статьи jpg')
    image_webp = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Обложка статьи webp')
    image_webp_small = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Small Обложка статьи webp')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published', verbose_name='Статус') 
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.CASCADE, related_name='videos', verbose_name='Марка авто')
    objects = models.Manager() # The default manager. 
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager(blank=True)

    class Meta: 
        ordering = ('-publish',) 

    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse('head:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.slug])


class Comment(models.Model): 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Название статьи')
    name = models.CharField(max_length=80, verbose_name='Ваше имя') 
    email = models.EmailField(verbose_name='Ваш e-mail') 
    body = models.TextField(verbose_name='Комментарий') 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
 
    class Meta: 
        ordering = ('created',) 
 
    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post)
