from django.contrib import admin
from .models import Ad, AdImage


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'slug', 'description', 'price', 'discount', 'latitude', 'longitude', 'views', 'likes']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'name', 'slug', 'description', 'price', 'discount', 'latitude', 'longitude', 'views', 'likes']
    search_fields = ['name', 'slug', 'price']


@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']