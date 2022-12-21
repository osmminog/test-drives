from django.shortcuts import render, get_object_or_404
from .models import Brand, Car, CarVideo, Post, Comment
from datetime import datetime
#from .mixins import findyoutube, save_video
#from .parser_news import parse_posts
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.postgres.search import TrigramSimilarity
from django.template.defaultfilters import slugify, truncatewords


now = datetime.now()


#обработчик страницы 404
def error_404_view(request, exception):
    popularvideo = CarVideo.objects.all().order_by('-number_of_views')
    popularvideo = popularvideo.filter(available=True)[:4]
    return render(request, '404.html', {'popularvideo': popularvideo,})


#обработчик страниц популярные видео
def head_page(request, brand_slug=None):
    brand = None
    brands = Brand.objects.all()
    car = None
    cars = Car.objects.filter(available=True)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        cars = cars.filter(brand=brand)
    slug = None
    #получаем все видео из базы данных
    popularvideo = CarVideo.objects.all().order_by('-number_of_views')
    #если выбран бренд фильтруем
    if  brand_slug:
        popularvideo = popularvideo.filter(brand=brand, available=True)[:500]
    else:
        popularvideo = popularvideo.filter(available=True)[:4]
    newvideo = CarVideo.objects.all().order_by('-age')
    newvideo = newvideo.filter(available=True)[:4]

    posts = Post.published.all()[1:5]
    new_post = Post.published.all().order_by('-publish')[:1]

    return render(request, 'head/lists/head_page.html', {'new_post': new_post, 'posts': posts, 'brand': brand, 'brands': brands, 'cars': cars, 'car': car, 'popularvideo': popularvideo, 'slug': slug, 'now': now, 'newvideo': newvideo,})


#обработчик страниц популярные видео
def popular_list(request, brand_slug=None):
    brand = None
    brands = Brand.objects.all()
    car = None
    cars = Car.objects.filter(available=True)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        cars = cars.filter(brand=brand)
    slug = 'popular_video/'
    #получаем все видео из базы данных
    popularvideo = CarVideo.objects.all().order_by('-number_of_views')
    #если выбран бренд фильтруем
    if  brand_slug:
        popularvideo = popularvideo.filter(brand=brand, available=True)[:500]
    else:
        popularvideo = popularvideo.filter(available=True)[:500]
    newvideo = CarVideo.objects.all().order_by('-age')
    newvideo = newvideo.filter(available=True)[:4]

    return render(request, 'head/lists/popular_video.html', {'slug': slug, 'brand': brand, 'brands': brands, 'cars': cars, 'car': car, 'popularvideo': popularvideo, 'slug': slug, 'now': now, 'newvideo': newvideo,})


#обработчик страницы новых видео
def new_video_list(request, brand_slug=None, car_slug=None):
    brand = None
    brands = Brand.objects.all()
    car = None
    cars = Car.objects.all()
    cars = Car.objects.filter(available=True)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        cars = cars.filter(brand=brand)
    if car_slug:
        car = get_object_or_404(Car, slug=car_slug)
    slug = 'new_video/'

    newvideos = CarVideo.objects.all()
    newvideos = CarVideo.objects.all().order_by('-age')
    newvideos = newvideos.filter(available=True)[:500]
    popularvideo = CarVideo.objects.all().order_by('-number_of_views')
    popularvideo = popularvideo.filter(available=True)[:4]
    return render(request, 'head/lists/new_video.html', {'brands': brands, 'cars': cars, 'brand': brand, 'car': car, 'newvideos': newvideos, 'slug': slug, 'now': now, 'popularvideo': popularvideo,})


#обработчик страниц видео по брендам
def brand_list(request, brand_slug=None):
    brand = None
    brands = Brand.objects.all()
    car = None
    cars = Car.objects.filter(available=True)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        cars = cars.filter(brand=brand)
    slug = brand_slug
    #получаем все видео из базы данных
    brandvideo = CarVideo.objects.all().order_by('-number_of_views')
    #если выбран бренд фильтруем
    if  brand_slug:
        brandvideo = brandvideo.filter(brand=brand, available=True)[:500]
    else:
        brandvideo = brandvideo.filter(available=True)[:500]
    newvideo = CarVideo.objects.all().order_by('-age')
    newvideo = newvideo.filter(available=True)[:4]

    return render(request, 'head/lists/brand_video.html', {'brand': brand, 'brands': brands, 'cars': cars, 'car': car, 'brandvideo': brandvideo, 'slug': slug, 'now': now, 'newvideo': newvideo,})


#обработчик страниц по моделям
def car_list(request, brand_slug=None, car_slug=None):
    brand = None
    brands = Brand.objects.all()
    car = None
    cars = Car.objects.all()
    cars = Car.objects.filter(available=True)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        cars = cars.filter(brand=brand)
    if car_slug:
        car = get_object_or_404(Car, slug=car_slug)
    slug = car_slug
    # #фильтр за все время по количеству просмотров
    # filtr = '&sp=CAMSAhAB'
    # links, titles, number_of_views, image_urls, id_videos, hq, date, text_date = findyoutube('Тест драйв ' + str(brand) + str(car), filtr)
    # #Запись в модель CarVideo новых данных
    # save_video(titles, number_of_views, image_urls, id_videos, brand, car, hq, date, text_date)

    # #фильтр за все время по дате загрузки
    # filtr = '&sp=CAI%253D'
    # links, titles, number_of_views, image_urls, id_videos, hq, date, text_date = findyoutube('Тест драйв ' + str(brand) + str(car), filtr)
    # #Запись в модель CarVideo новых данных
    # save_video(titles, number_of_views, image_urls, id_videos, brand, car, hq, date, text_date)
                
    carvideo = CarVideo.objects.all().order_by('-number_of_views')
    carvideo = carvideo.filter(brand=brand, car=car, available=True)
    newvideo = CarVideo.objects.all().order_by('-age')
    newvideo = newvideo.filter(available=True)[:4]
    
    return render(request, 'head/lists/car_video.html', {'brands': brands, 'cars': cars, 'brand': brand, 'car': car, 'slug': slug, 'carvideo': carvideo, 'now': now, 'newvideo': newvideo,})


def post_list(request, tag_slug=None, brand_slug=None, car_slug=None):
    brand = None
    brands = Brand.objects.all()
    car = None
    cars = Car.objects.all()
    cars = Car.objects.filter(available=True)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        cars = cars.filter(brand=brand)
    if car_slug:
        car = get_object_or_404(Car, slug=car_slug)

    object_list = Post.published.all()
    tag = None
    posts = Post.published.all()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
        posts = object_list

    video = CarVideo.objects.all().order_by('-number_of_views')
    video = video.filter(available=True)[:4]
    slug = 'autonews/'
    return render(request, 'head/lists/posts.html', {'posts': posts, 'slug': slug, 'tag': tag, 'brands': brands, 'cars': cars, 'brand': brand, 'car': car, 'video': video, })

                  
def post_detail(request, year, month, post, brand_slug=None, car_slug=None,):
    brand = None
    brands = Brand.objects.all()
    car = None
    cars = Car.objects.all()
    cars = Car.objects.filter(available=True)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        cars = cars.filter(brand=brand)
    if car_slug:
        car = get_object_or_404(Car, slug=car_slug)
    
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month)

    description = truncatewords(post.body, 30)

    # Список активных комментариев для этой статьи
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Пользователь отправил комментарий
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье
            new_comment.post = post
            # Сохраняем комментарий в базе данных
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Формирование списка похожих статей
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    
    video = CarVideo.objects.all().order_by('-number_of_views')
    brand_name = post.brand
    slug_brand = str(brand_name).lower()
    video_brand = video.filter(brand=post.brand, available=True)[:4]
    video = video.filter(available=True)[:4]
    slug = post.slug

    return render(request, 'head/lists/post_detail.html',
                  {'post': post,
                   'slug': slug,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts, 
                   'brands': brands, 
                   'cars': cars, 
                   'brand': brand, 
                   'car': car, 
                   'brand_name': brand_name,
                   'slug_brand': slug_brand,
                   'video_brand': video_brand,
                   'video': video,
                   'description': description,
                   })


def post_share(request, post_id, brand_slug=None):
    brand = None
    brands = Brand.objects.all()
    car = None
    cars = Car.objects.filter(available=True)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        cars = cars.filter(brand=brand)

    # Получение статьи по идентификатору
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False 
 
    if request.method == 'POST':
        # Форма была отправлена на сохранение
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, u'message', 'admin@test-drives.ru', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    slug = 'share/'
    return render(request, 'head/lists/share.html', {'post': post, 'slug': slug, 'form': form, 'sent': sent, 'brands': brands, 'cars': cars, 'brand': brand, 'car': car,})


# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.objects.annotate(
#                 similarity=TrigramSimilarity('title', query),
#             ).filter(similarity__gt=0.3).order_by('-similarity')
#     return render(request,
#                   'head/search.html',
#                   {'form': form,
#                    'query': query,
#                    'results': results})