from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('images/', include('head.urls', namespace='head_image')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('head.urls', namespace='head')),
    path('chaining/', include('smart_selects.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),),
]

handler404 = 'head.views.error_404_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

