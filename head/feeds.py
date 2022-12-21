from yaturbo import YandexTurboFeed
from django.template.defaultfilters import truncatewords
from .models import Post
from datetime import datetime


class TurboFeed(YandexTurboFeed):
    title = 'News'
    link = '/autonews/'
    description = 'News about cars.'

    def items(self):
        post = Post.objects.all()
        post = post.filter(status='published')
        return post[:15]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.publish

    def item_turbo(self, item):
        return '\n<figure><img src="/media/{}" alt="{}"></figure>\n{}'.format(item.image_jpg, item.title, truncatewords(item.body, 50) )


