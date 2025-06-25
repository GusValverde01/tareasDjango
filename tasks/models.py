from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Category(models.Model):
    """Categorías para clasificar el contenido"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Genre(models.Model):
    """Géneros para clasificar el contenido"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    
    class Meta:
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ContentItem(models.Model):
    """Modelo base para todo tipo de contenido multimedial"""
    CONTENT_TYPES = [
        ('movie', 'Película'),
        ('series', 'Serie'),
        ('book', 'Libro'),
        ('anime', 'Anime'),
        ('videogame', 'Videojuego'),
    ]
    
    title = models.CharField(max_length=300, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, verbose_name='Tipo de contenido')
    release_date = models.DateField(null=True, blank=True, verbose_name='Fecha de lanzamiento')
    duration = models.IntegerField(null=True, blank=True, verbose_name='Duración (minutos)')
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        null=True, blank=True, verbose_name='Calificación'
    )
    image_url = models.URLField(null=True, blank=True, verbose_name='URL de imagen')
    trailer_url = models.URLField(null=True, blank=True, verbose_name='URL de trailer')
    director = models.CharField(max_length=200, null=True, blank=True, verbose_name='Director')
    author = models.CharField(max_length=200, null=True, blank=True, verbose_name='Autor')
    studio = models.CharField(max_length=200, null=True, blank=True, verbose_name='Estudio/Editorial')
    platform = models.CharField(max_length=200, null=True, blank=True, verbose_name='Plataforma')
    
    # Relaciones
    genres = models.ManyToManyField(Genre, blank=True, verbose_name='Géneros')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Categoría')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Contenido'
        verbose_name_plural = 'Contenidos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type']),
            models.Index(fields=['title']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"

class UserProfile(models.Model):
    """Perfil extendido del usuario para recomendaciones"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    favorite_genres = models.ManyToManyField(Genre, blank=True, verbose_name='Géneros favoritos')
    favorite_content_types = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name='Tipos de contenido favoritos'
    )
    bio = models.TextField(blank=True, verbose_name='Biografía')
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

class Rating(models.Model):
    """Calificaciones de usuarios para contenido"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    content = models.ForeignKey(ContentItem, on_delete=models.CASCADE, verbose_name='Contenido', related_name='user_ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Calificación'
    )
    review = models.TextField(blank=True, verbose_name='Reseña')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        unique_together = ['user', 'content']
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.content.title}: {self.rating}/5"

class Favorite(models.Model):
    """Lista de favoritos del usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    content = models.ForeignKey(ContentItem, on_delete=models.CASCADE, verbose_name='Contenido')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de adición')
    
    class Meta:
        unique_together = ['user', 'content']
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.content.title}"

class SearchHistory(models.Model):
    """Historial de búsquedas para mejorar recomendaciones"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    query = models.CharField(max_length=500, verbose_name='Consulta')
    content_type_filter = models.CharField(max_length=20, blank=True, verbose_name='Filtro de tipo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de búsqueda')
    
    class Meta:
        verbose_name = 'Historial de Búsqueda'
        verbose_name_plural = 'Historiales de Búsqueda'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.query}"


