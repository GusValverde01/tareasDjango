"""
URL configuration for Sistema de Búsqueda y Recomendación Multimodal.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path('content/<int:content_id>/', views.content_detail, name='content_detail'),
    path('rate/<int:content_id>/', views.rate_content, name='rate_content'),
    path('favorite/<int:content_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.user_favorites, name='user_favorites'),
    path('profile/', views.user_profile, name='user_profile'),
    path('import-content/', views.import_external_content, name='import_external_content'),
    path('test-apis/', views.test_apis, name='test_apis'),
]
