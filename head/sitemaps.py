from django.contrib.sitemaps import Sitemap
from .models import Car, Brand, Post
from django.urls import reverse
from django.contrib import sitemaps


class BrandSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Brand.objects.all()


class CarSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    
    def items(self):
        return Car.objects.all()


class HeadPageSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['head:popular_list']

    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    
    def items(self):
        return Post.objects.all()