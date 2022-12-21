from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BrandSitemap, CarSitemap, HeadPageSitemap, PostSitemap
from head.feeds import TurboFeed


sitemaps = {'static': HeadPageSitemap, 'brand': BrandSitemap, 'cars': CarSitemap, 'post': PostSitemap}

app_name = 'head'

urlpatterns = [
    path('', views.head_page, name='head_page'),
    path('popular_video/', views.popular_list, name='popular_list'),
    path('new_video/', views.new_video_list, name='new_video_list'),
    path('autonews/', views.post_list, name='post_list'),
    path('feeds/turbo/', TurboFeed()),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<slug:brand_slug>/', views.brand_list, name='video_list_by_brand'),
    path('<slug:brand_slug>/<slug:car_slug>/', views.car_list, name='video_list_by_car'),    
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
