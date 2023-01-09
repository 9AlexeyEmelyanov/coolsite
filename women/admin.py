from django.contrib import admin
from .models import Women, Category



@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published',)
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):    
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('title',)

