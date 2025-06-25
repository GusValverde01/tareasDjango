"""
Servicios para integrar APIs externas de contenido multimedia
APIs sin credenciales utilizadas:
- TVMaze API (series/shows)
- Jikan API (anime)
- Open Library API (libros)
- Google Books API (libros)
"""

import requests
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseAPIService:
    """Clase base para servicios de API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MediaFind/1.0 (Educational Project)'
        })
    
    def make_request(self, url, params=None):
        """Realizar petición HTTP con manejo de errores"""
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error en petición a {url}: {e}")
            return None


class TVMazeAPIService(BaseAPIService):
    """Servicio para TVMaze API - Series y Shows"""
    
    BASE_URL = "https://api.tvmaze.com"
    
    def search_shows(self, query, limit=10):
        """Buscar series por nombre"""
        url = f"{self.BASE_URL}/search/shows"
        params = {'q': query}
        
        data = self.make_request(url, params)
        if not data:
            return []
        
        results = []
        for item in data[:limit]:
            show = item.get('show', {})
            results.append(self._format_show_data(show))
        
        return results
    
    def get_show_details(self, tvmaze_id):
        """Obtener detalles de una serie específica"""
        url = f"{self.BASE_URL}/shows/{tvmaze_id}"
        
        data = self.make_request(url)
        if not data:
            return None
        
        return self._format_show_data(data)
    
    def _format_show_data(self, show_data):
        """Formatear datos de serie para nuestro modelo"""
        return {
            'external_id': show_data.get('id'),
            'title': show_data.get('name', 'Sin título'),
            'description': self._clean_html(show_data.get('summary', '')),
            'content_type': 'series',
            'release_date': self._parse_date(show_data.get('premiered')),
            'rating': show_data.get('rating', {}).get('average'),
            'image_url': show_data.get('image', {}).get('medium') if show_data.get('image') else None,
            'genres': show_data.get('genres', []),
            'studio': show_data.get('network', {}).get('name') if show_data.get('network') else None,
            'duration': show_data.get('averageRuntime'),
            'status': show_data.get('status'),
            'language': show_data.get('language'),
            'external_urls': {
                'tvmaze': show_data.get('url'),
                'imdb': f"https://imdb.com/title/{show_data.get('externals', {}).get('imdb')}" if show_data.get('externals', {}).get('imdb') else None
            }
        }
    
    def _clean_html(self, text):
        """Limpiar HTML de las descripciones"""
        if not text:
            return ''
        import re
        return re.sub(r'<[^>]+>', '', text).strip()
    
    def _parse_date(self, date_str):
        """Convertir string de fecha a objeto date"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            return None


class JikanAPIService(BaseAPIService):
    """Servicio para Jikan API - Anime"""
    
    BASE_URL = "https://api.jikan.moe/v4"
    
    def search_anime(self, query, limit=10):
        """Buscar anime por nombre"""
        url = f"{self.BASE_URL}/anime"
        params = {
            'q': query,
            'limit': limit,
            'order_by': 'score',
            'sort': 'desc'
        }
        
        data = self.make_request(url, params)
        if not data or 'data' not in data:
            return []
        
        results = []
        for anime in data['data']:
            results.append(self._format_anime_data(anime))
        
        return results
    
    def get_anime_details(self, mal_id):
        """Obtener detalles de un anime específico"""
        url = f"{self.BASE_URL}/anime/{mal_id}/full"
        
        data = self.make_request(url)
        if not data or 'data' not in data:
            return None
        
        return self._format_anime_data(data['data'])
    
    def _format_anime_data(self, anime_data):
        """Formatear datos de anime para nuestro modelo"""
        return {
            'external_id': anime_data.get('mal_id'),
            'title': anime_data.get('title', 'Sin título'),
            'description': anime_data.get('synopsis', ''),
            'content_type': 'anime',
            'release_date': self._parse_date(anime_data.get('aired', {}).get('from')),
            'rating': anime_data.get('score'),
            'image_url': anime_data.get('images', {}).get('jpg', {}).get('image_url'),
            'trailer_url': anime_data.get('trailer', {}).get('url'),
            'genres': [genre['name'] for genre in anime_data.get('genres', [])],
            'studio': anime_data.get('studios', [{}])[0].get('name') if anime_data.get('studios') else None,
            'duration': anime_data.get('duration'),
            'episodes': anime_data.get('episodes'),
            'status': anime_data.get('status'),
            'external_urls': {
                'mal': anime_data.get('url'),
                'trailer': anime_data.get('trailer', {}).get('url')
            }
        }
    
    def _parse_date(self, date_str):
        """Convertir string de fecha ISO a objeto date"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
        except:
            return None


class OpenLibraryAPIService(BaseAPIService):
    """Servicio para Open Library API - Libros"""
    
    BASE_URL = "https://openlibrary.org"
    
    def search_books(self, query, limit=10):
        """Buscar libros por título o autor"""
        url = f"{self.BASE_URL}/search.json"
        params = {
            'q': query,
            'limit': limit,
            'fields': 'key,title,author_name,first_publish_year,isbn,cover_i,subject,publisher'
        }
        
        data = self.make_request(url, params)
        if not data or 'docs' not in data:
            return []
        
        results = []
        for book in data['docs']:
            results.append(self._format_book_data(book))
        
        return results
    
    def get_book_details(self, ol_key):
        """Obtener detalles de un libro específico"""
        url = f"{self.BASE_URL}{ol_key}.json"
        
        data = self.make_request(url)
        if not data:
            return None
        
        return self._format_book_details(data)
    
    def _format_book_data(self, book_data):
        """Formatear datos de búsqueda de libro"""
        cover_id = book_data.get('cover_i')
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None
        
        return {
            'external_id': book_data.get('key', '').replace('/works/', ''),
            'title': book_data.get('title', 'Sin título'),
            'description': '',  # No disponible en búsqueda básica
            'content_type': 'book',
            'release_date': self._get_first_publish_year(book_data.get('first_publish_year')),
            'image_url': cover_url,
            'author': ', '.join(book_data.get('author_name', [])),
            'genres': book_data.get('subject', [])[:5],  # Primeros 5 temas
            'studio': ', '.join(book_data.get('publisher', [])[:3]) if book_data.get('publisher') else None,
            'isbn': book_data.get('isbn', [None])[0],
            'external_urls': {
                'openlibrary': f"https://openlibrary.org{book_data.get('key', '')}"
            }
        }
    
    def _format_book_details(self, book_data):
        """Formatear detalles completos de libro"""
        description = ''
        if isinstance(book_data.get('description'), dict):
            description = book_data['description'].get('value', '')
        elif isinstance(book_data.get('description'), str):
            description = book_data['description']
        
        return {
            'external_id': book_data.get('key', '').replace('/works/', ''),
            'title': book_data.get('title', 'Sin título'),
            'description': description,
            'content_type': 'book',
            'subjects': book_data.get('subjects', []),
            'external_urls': {
                'openlibrary': f"https://openlibrary.org{book_data.get('key', '')}"
            }
        }
    
    def _get_first_publish_year(self, year):
        """Convertir año de publicación a fecha"""
        if not year:
            return None
        try:
            return datetime(year, 1, 1).date()
        except:
            return None


class GoogleBooksAPIService(BaseAPIService):
    """Servicio para Google Books API - Libros"""
    
    BASE_URL = "https://www.googleapis.com/books/v1"
    
    def search_books(self, query, limit=10):
        """Buscar libros en Google Books"""
        url = f"{self.BASE_URL}/volumes"
        params = {
            'q': query,
            'maxResults': min(limit, 40),  # Google Books max es 40
            'orderBy': 'relevance'
        }
        
        data = self.make_request(url, params)
        if not data or 'items' not in data:
            return []
        
        results = []
        for item in data['items'][:limit]:
            results.append(self._format_google_book_data(item))
        
        return results
    
    def get_book_details(self, google_id):
        """Obtener detalles de un libro específico"""
        url = f"{self.BASE_URL}/volumes/{google_id}"
        
        data = self.make_request(url)
        if not data:
            return None
        
        return self._format_google_book_data(data)
    
    def _format_google_book_data(self, book_data):
        """Formatear datos de Google Books"""
        volume_info = book_data.get('volumeInfo', {})
        
        # Obtener la mejor imagen disponible
        image_links = volume_info.get('imageLinks', {})
        image_url = (image_links.get('large') or 
                    image_links.get('medium') or 
                    image_links.get('small') or 
                    image_links.get('thumbnail'))
        
        return {
            'external_id': book_data.get('id'),
            'title': volume_info.get('title', 'Sin título'),
            'description': volume_info.get('description', ''),
            'content_type': 'book',
            'release_date': self._parse_google_date(volume_info.get('publishedDate')),
            'image_url': image_url,
            'author': ', '.join(volume_info.get('authors', [])),
            'genres': volume_info.get('categories', []),
            'studio': volume_info.get('publisher'),
            'page_count': volume_info.get('pageCount'),
            'language': volume_info.get('language'),
            'isbn': self._get_isbn(volume_info.get('industryIdentifiers', [])),
            'rating': volume_info.get('averageRating'),
            'external_urls': {
                'google_books': volume_info.get('infoLink'),
                'preview': volume_info.get('previewLink')
            }
        }
    
    def _parse_google_date(self, date_str):
        """Convertir fecha de Google Books a objeto date"""
        if not date_str:
            return None
        try:
            # Google Books puede devolver solo año, año-mes o fecha completa
            if len(date_str) == 4:  # Solo año
                return datetime(int(date_str), 1, 1).date()
            elif len(date_str) == 7:  # Año-mes
                return datetime.strptime(date_str, '%Y-%m').date()
            else:  # Fecha completa
                return datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            return None
    
    def _get_isbn(self, identifiers):
        """Extraer ISBN de los identificadores"""
        for identifier in identifiers:
            if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
                return identifier.get('identifier')
        return None


# Instancias globales de los servicios
tvmaze_service = TVMazeAPIService()
jikan_service = JikanAPIService()
openlibrary_service = OpenLibraryAPIService()
googlebooks_service = GoogleBooksAPIService()


def search_content_from_apis(query, content_type=None, limit=10):
    """
    Buscar contenido en todas las APIs disponibles
    """
    results = []
    
    if not content_type or content_type == 'series':
        # Buscar series en TVMaze
        try:
            series_results = tvmaze_service.search_shows(query, limit)
            results.extend(series_results)
        except Exception as e:
            logger.error(f"Error buscando series: {e}")
    
    if not content_type or content_type == 'anime':
        # Buscar anime en Jikan
        try:
            anime_results = jikan_service.search_anime(query, limit)
            results.extend(anime_results)
        except Exception as e:
            logger.error(f"Error buscando anime: {e}")
    
    if not content_type or content_type == 'book':
        # Buscar libros en Open Library y Google Books
        try:
            ol_results = openlibrary_service.search_books(query, limit//2)
            gb_results = googlebooks_service.search_books(query, limit//2)
            results.extend(ol_results)
            results.extend(gb_results)
        except Exception as e:
            logger.error(f"Error buscando libros: {e}")
    
    return results[:limit]


def import_content_to_database(api_data):
    """
    Importar contenido de APIs a nuestra base de datos
    """
    from tasks.models import ContentItem, Genre
    
    try:
        # Verificar si ya existe
        existing = ContentItem.objects.filter(
            title=api_data['title'],
            content_type=api_data['content_type']
        ).first()
        
        if existing:
            return existing
        
        # Crear nuevo contenido
        content_data = {
            'title': api_data['title'],
            'description': api_data.get('description', ''),
            'content_type': api_data['content_type'],
            'release_date': api_data.get('release_date'),
            'rating': api_data.get('rating'),
            'image_url': api_data.get('image_url'),
            'trailer_url': api_data.get('trailer_url'),
            'director': api_data.get('director'),
            'author': api_data.get('author'),
            'studio': api_data.get('studio'),
            'platform': api_data.get('platform'),
        }
        
        # Filtrar valores None
        content_data = {k: v for k, v in content_data.items() if v is not None}
        
        content = ContentItem.objects.create(**content_data)
        
        # Agregar géneros
        genres = api_data.get('genres', [])
        for genre_name in genres[:5]:  # Máximo 5 géneros
            if genre_name:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                content.genres.add(genre)
        
        return content
        
    except Exception as e:
        logger.error(f"Error importando contenido: {e}")
        return None
