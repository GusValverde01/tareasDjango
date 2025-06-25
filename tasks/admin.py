from django.contrib import admin
from .models import ContentItem, Category, Genre, Rating, Favorite, SearchHistory, UserProfile

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'rating', 'release_date', 'created_at']
    list_filter = ['content_type', 'genres', 'category', 'release_date']
    search_fields = ['title', 'description', 'director', 'author', 'studio']
    filter_horizontal = ['genres']
    list_editable = ['rating']
    date_hierarchy = 'release_date'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'description', 'content_type', 'category')
        }),
        ('Detalles', {
            'fields': ('release_date', 'duration', 'rating', 'genres')
        }),
        ('Metadatos', {
            'fields': ('director', 'author', 'studio', 'platform')
        }),
        ('Multimedia', {
            'fields': ('image_url', 'trailer_url')
        }),
    )

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'content__title']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'content__title']

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query', 'content_type_filter', 'created_at']
    list_filter = ['content_type_filter', 'created_at']
    search_fields = ['user__username', 'query']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_content_types']
    filter_horizontal = ['favorite_genres']
    search_fields = ['user__username']
