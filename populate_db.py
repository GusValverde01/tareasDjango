"""
Script para poblar la base de datos con datos de ejemplo
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tareasDj4ngo.settings')
django.setup()

from tasks.models import Category, Genre, ContentItem, UserProfile
from django.contrib.auth.models import User
from datetime import date

def create_sample_data():
    print("Creando datos de ejemplo...")
    
    # Crear categorías
    categories = [
        {'name': 'Acción', 'description': 'Contenido lleno de acción y aventura'},
        {'name': 'Drama', 'description': 'Historias dramáticas y emocionales'},
        {'name': 'Comedia', 'description': 'Contenido humorístico y divertido'},
        {'name': 'Ciencia Ficción', 'description': 'Historias futuristas y tecnológicas'},
        {'name': 'Fantasy', 'description': 'Mundos mágicos y fantásticos'},
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"Categoría creada: {category.name}")
    
    # Crear géneros
    genres = [
        'Acción', 'Aventura', 'Comedia', 'Drama', 'Terror', 'Thriller',
        'Romance', 'Ciencia Ficción', 'Fantasy', 'Misterio', 'Crimen',
        'Documentales', 'Biografía', 'Historia', 'Guerra', 'Western',
        'Musical', 'Animación', 'Superhéroes', 'Deportes'
    ]
    
    for genre_name in genres:
        genre, created = Genre.objects.get_or_create(name=genre_name)
        if created:
            print(f"Género creado: {genre.name}")
    
    # Crear contenido de ejemplo
    content_items = [
        # Películas
        {
            'title': 'Avengers: Endgame',
            'description': 'Los Vengadores se enfrentan a su desafío más grande en esta épica conclusión.',
            'content_type': 'movie',
            'release_date': date(2019, 4, 26),
            'duration': 181,
            'rating': 8.4,
            'director': 'Anthony y Joe Russo',
            'studio': 'Marvel Studios',
            'genres': ['Acción', 'Aventura', 'Superhéroes']
        },
        {
            'title': 'Inception',
            'description': 'Un ladrón especializado en extracción de secretos del subconsciente durante el estado de sueño.',
            'content_type': 'movie',
            'release_date': date(2010, 7, 16),
            'duration': 148,
            'rating': 8.8,
            'director': 'Christopher Nolan',
            'studio': 'Warner Bros',
            'genres': ['Acción', 'Ciencia Ficción', 'Thriller']
        },
        {
            'title': 'The Dark Knight',
            'description': 'Batman se enfrenta al Joker en una batalla por el alma de Gotham City.',
            'content_type': 'movie',
            'release_date': date(2008, 7, 18),
            'duration': 152,
            'rating': 9.0,
            'director': 'Christopher Nolan',
            'studio': 'Warner Bros',
            'genres': ['Acción', 'Crimen', 'Drama']
        },
        
        # Series
        {
            'title': 'Breaking Bad',
            'description': 'Un profesor de química se convierte en fabricante de metanfetaminas.',
            'content_type': 'series',
            'release_date': date(2008, 1, 20),
            'rating': 9.5,
            'studio': 'AMC',
            'genres': ['Drama', 'Crimen', 'Thriller']
        },
        {
            'title': 'Game of Thrones',
            'description': 'Nueve familias nobles luchan por el control del mítico reino de Westeros.',
            'content_type': 'series',
            'release_date': date(2011, 4, 17),
            'rating': 9.3,
            'studio': 'HBO',
            'genres': ['Drama', 'Fantasy', 'Aventura']
        },
        
        # Libros
        {
            'title': 'Harry Potter y la Piedra Filosofal',
            'description': 'Un joven mago descubre su verdadera identidad en su undécimo cumpleaños.',
            'content_type': 'book',
            'release_date': date(1997, 6, 26),
            'rating': 8.7,
            'author': 'J.K. Rowling',
            'studio': 'Bloomsbury',
            'genres': ['Fantasy', 'Aventura']
        },
        {
            'title': 'El Señor de los Anillos: La Comunidad del Anillo',
            'description': 'Un hobbit emprende una épica aventura para destruir un anillo mágico.',
            'content_type': 'book',
            'release_date': date(1954, 7, 29),
            'rating': 9.2,
            'author': 'J.R.R. Tolkien',
            'studio': 'George Allen & Unwin',
            'genres': ['Fantasy', 'Aventura']
        },
        
        # Anime
        {
            'title': 'Attack on Titan',
            'description': 'La humanidad lucha por sobrevivir contra gigantes devoradores de humanos.',
            'content_type': 'anime',
            'release_date': date(2013, 4, 7),
            'rating': 9.0,
            'director': 'Tetsuro Araki',
            'studio': 'Studio Pierrot',
            'genres': ['Acción', 'Drama', 'Fantasy']
        },
        {
            'title': 'Death Note',
            'description': 'Un estudiante encuentra un cuaderno sobrenatural que puede matar a cualquiera.',
            'content_type': 'anime',
            'release_date': date(2006, 10, 4),
            'rating': 9.0,
            'director': 'Tetsuro Araki',
            'studio': 'Madhouse',
            'genres': ['Thriller', 'Misterio', 'Crimen']
        },
        
        # Videojuegos
        {
            'title': 'The Legend of Zelda: Breath of the Wild',
            'description': 'Link despierta en un mundo post-apocalíptico y debe salvar Hyrule.',
            'content_type': 'videogame',
            'release_date': date(2017, 3, 3),
            'rating': 9.7,
            'studio': 'Nintendo',
            'platform': 'Nintendo Switch',
            'genres': ['Aventura', 'Acción']
        },
        {
            'title': 'The Witcher 3: Wild Hunt',
            'description': 'Geralt de Rivia busca a su hija adoptiva en un mundo lleno de monstruos.',
            'content_type': 'videogame',
            'release_date': date(2015, 5, 19),
            'rating': 9.3,
            'studio': 'CD Projekt Red',
            'platform': 'PC, PlayStation, Xbox',
            'genres': ['Aventura', 'Fantasy']
        }
    ]
    
    for item_data in content_items:
        genres_list = item_data.pop('genres', [])
        content, created = ContentItem.objects.get_or_create(
            title=item_data['title'],
            defaults=item_data
        )
        
        if created:
            # Asignar géneros
            for genre_name in genres_list:
                try:
                    genre = Genre.objects.get(name=genre_name)
                    content.genres.add(genre)
                except Genre.DoesNotExist:
                    print(f"Género no encontrado: {genre_name}")
            
            print(f"Contenido creado: {content.title}")
    
    print("¡Datos de ejemplo creados exitosamente!")

if __name__ == '__main__':
    create_sample_data()
