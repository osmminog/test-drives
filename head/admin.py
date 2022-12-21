from django.contrib import admin
from django.db import models
from django.db.models import fields
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Post, Comment, Brand, Car, CarVideo
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


admin.site.site_title = "Тест драйвы"
admin.site.site_header = format_html("<img src='http://127.0.0.1:8000/static/img/Logo.svg' height=50 width=50>")


class BrandAdminForm(forms.ModelForm):
    history = forms.CharField(label='История марки', widget=CKEditorUploadingWidget(), required=False)  
    class Meta:
        model = Brand
        fields = '__all__'


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(label='Текст статьи', widget=CKEditorUploadingWidget(), required=False)   
    class Meta:
        model = Post
        fields = '__all__'


class CarVideoResource(resources.ModelResource):
    class Meta:
        model = CarVideo


class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand


class CarResource(resources.ModelResource):
    class Meta:
        model = Car 

class PostResource(resources.ModelResource):
    class Meta:
        model = Post
   

class CarInlineAdmin(admin.StackedInline):
    model = Car


@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    list_display = ('title', 'slug',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    inlines = [CarInlineAdmin,]
    resource_class = BrandResource
    form = BrandAdminForm
    

@admin.register(Car)
class CarAdmin(ImportExportModelAdmin):
    list_display = ('title', 'slug',)
    list_filter = ('available',)
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    resource_class = CarResource


@admin.register(CarVideo)
class CarVideoAdmin(ImportExportModelAdmin):
    list_display = ('title_video', 'age', 'created', 'brand', 'car', 'available',)
    search_fields = ('title_video',)
    save_on_top = True
    list_editable = ('available',)
    readonly_fields = ('age', 'id_videos', 'number_of_views', 'hq', 'image_urls', 'url', 'image_jpg_image', 'image_webp_image', 'image_webp_small_image')
    list_filter = (
        ('brand', RelatedDropdownFilter), 
        ('car', RelatedDropdownFilter), 
        'age',
        'available',
        )
    def image_jpg_image(self, obj):
        return mark_safe('<img src="{url}" width="160" height="100" />'.format(
            url = obj.image_jpg.url,
            )
    )
    def image_webp_image(self, obj):
        return mark_safe('<img src="{url}" width="160" height="100" />'.format(
            url = obj.image_webp.url,
            )
    )
    def image_webp_small_image(self, obj):
        return mark_safe('<img src="{url}" width="140" height="80" />'.format(
            url = obj.image_webp_small.url,
            )
    )
    fieldsets = (
         (None, {
            'fields': ('title_video', 'brand', 'car', 'available', 'age', 'number_of_views', 'id_videos')
        }),
        ('Изображения', {
            'classes': ('collapse',),
            'fields': (
                ('image_jpg', 'image_jpg_image'), 
                ('image_webp', 'image_webp_image'), 
                ('image_webp_small', 'image_webp_small_image'),
            ),
        }),
    )        
    resource_class = CarVideoResource
    list_per_page = 250


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'brand')
    search_fields = ('title', 'publish',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    form = PostAdminForm
    resource_class = PostResource
    readonly_fields = ('image_jpg_image', 'image_webp_image', 'image_webp_small_image')
    def image_jpg_image(self, obj):
        return mark_safe('<img src="{url}" width="160" height="100" />'.format(
            url = obj.image_jpg.url,
            )
    )
    def image_webp_image(self, obj):
        return mark_safe('<img src="{url}" width="160" height="100" />'.format(
            url = obj.image_webp.url,
            )
    )
    def image_webp_small_image(self, obj):
        return mark_safe('<img src="{url}" width="140" height="80" />'.format(
            url = obj.image_webp_small.url,
            )
    )
    fieldsets = (
         (None, {
            'fields': ('title', 'slug', 'brand', 'description', 'body', 'publish', 'tags', 'status',)
        }),
        ('Изображения', {
            'classes': ('collapse',),
            'fields': (
                ('image_jpg', 'image_jpg_image'),
                ('image_webp', 'image_webp_image'), 
                ('image_webp_small', 'image_webp_small_image'),
            ),
        }),
    )        


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')