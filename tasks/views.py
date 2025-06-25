from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import ContentItem, Category, Genre, Rating, Favorite, SearchHistory, UserProfile
from .api_services import search_content_from_apis, import_content_to_database
import json

# Create your views here.
def hello(request):
    """Vista de login principal"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def register(request):
    """Vista de registro de usuarios"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'register.html')
        
        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        # Crear perfil de usuario
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('home')
    
    return render(request, 'register.html')

@login_required
def home(request):
    """Vista principal del sistema de recomendaciones"""    # Obtener contenido más popular
    popular_content = ContentItem.objects.annotate(
        avg_rating=Avg('user_ratings__rating'),
        rating_count=Count('user_ratings')
    ).filter(rating_count__gt=0).order_by('-avg_rating', '-rating_count')[:6]
    
    # Obtener contenido reciente
    recent_content = ContentItem.objects.order_by('-created_at')[:6]
    
    # Obtener favoritos del usuario
    user_favorites = Favorite.objects.filter(user=request.user).select_related('content')[:6]
    
    # Obtener recomendaciones basadas en géneros favoritos del usuario
    try:
        user_profile = request.user.userprofile
        favorite_genres = user_profile.favorite_genres.all()
        if favorite_genres:
            recommended_content = ContentItem.objects.filter(
                genres__in=favorite_genres
            ).distinct().exclude(
                id__in=user_favorites.values_list('content_id', flat=True)
            )[:6]
        else:
            recommended_content = []
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)
        recommended_content = []
    
    context = {
        'popular_content': popular_content,
        'recent_content': recent_content,
        'user_favorites': user_favorites,
        'recommended_content': recommended_content,
    }
    return render(request, 'home.html', context)

@login_required
def search(request):
    """Vista de búsqueda de contenido"""
    query = request.GET.get('q', '')
    content_type = request.GET.get('type', '')
    genre = request.GET.get('genre', '')
    sort_by = request.GET.get('sort', 'title')
    search_external = request.GET.get('external', False)
    
    # Buscar en APIs externas si se solicita
    external_results = []
    if search_external and query:
        try:
            external_results = search_content_from_apis(query, content_type, 10)
        except Exception as e:
            messages.error(request, f'Error al buscar contenido externo: {str(e)}')
    
    # Buscar en base de datos local
    results = ContentItem.objects.all()
    
    # Filtrar por consulta de texto
    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(director__icontains=query) |
            Q(author__icontains=query) |
            Q(studio__icontains=query)
        )
        # Guardar búsqueda en historial
        SearchHistory.objects.create(
            user=request.user,
            query=query,
            content_type_filter=content_type
        )
    
    # Filtrar por tipo de contenido
    if content_type:
        results = results.filter(content_type=content_type)
    
    # Filtrar por género
    if genre:
        results = results.filter(genres__name=genre)
      # Ordenar resultados
    if sort_by == 'rating':
        results = results.annotate(avg_rating=Avg('user_ratings__rating')).order_by('-avg_rating')
    elif sort_by == 'date':
        results = results.order_by('-release_date')
    else:
        results = results.order_by('title')
    
    # Paginación
    paginator = Paginator(results, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener datos para filtros
    content_types = ContentItem.CONTENT_TYPES
    genres = Genre.objects.all()
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'content_type': content_type,
        'genre': genre,
        'sort_by': sort_by,
        'content_types': content_types,
        'genres': genres,
        'external_results': external_results,
        'search_external': search_external,
    }
    return render(request, 'search.html', context)

@login_required
def content_detail(request, content_id):
    """Vista de detalle de contenido"""
    content = get_object_or_404(ContentItem, id=content_id)
    
    # Verificar si el usuario ya tiene una calificación
    user_rating = None
    try:
        user_rating = Rating.objects.get(user=request.user, content=content)
    except Rating.DoesNotExist:
        pass
    
    # Verificar si está en favoritos
    is_favorite = Favorite.objects.filter(user=request.user, content=content).exists()
      # Obtener todas las calificaciones
    ratings = Rating.objects.filter(content=content).select_related('user')
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    
    # Contenido relacionado (mismo género o tipo)
    related_content = ContentItem.objects.filter(
        Q(genres__in=content.genres.all()) | Q(content_type=content.content_type)
    ).exclude(id=content.id).distinct()[:6]
    
    context = {
        'content': content,
        'user_rating': user_rating,
        'is_favorite': is_favorite,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'related_content': related_content,
    }
    return render(request, 'content_detail.html', context)

@login_required
def rate_content(request, content_id):
    """Calificar contenido"""
    if request.method == 'POST':
        content = get_object_or_404(ContentItem, id=content_id)
        rating_value = int(request.POST.get('rating'))
        review = request.POST.get('review', '')
        
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            content=content,
            defaults={'rating': rating_value, 'review': review}
        )
        
        messages.success(request, 'Calificación guardada exitosamente')
    
    return redirect('content_detail', content_id=content_id)

@login_required
def toggle_favorite(request, content_id):
    """Agregar o quitar de favoritos"""
    content = get_object_or_404(ContentItem, id=content_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        content=content
    )
    
    if not created:
        favorite.delete()
        action = 'removed'
    else:
        action = 'added'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'action': action})
    
    return redirect('content_detail', content_id=content_id)

@login_required
def user_favorites(request):
    """Vista de favoritos del usuario"""
    favorites = Favorite.objects.filter(user=request.user).select_related('content')
    
    # Paginación
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'favorites.html', context)

@login_required
def user_profile(request):
    """Vista y edición del perfil de usuario"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Actualizar perfil
        profile.bio = request.POST.get('bio', '')
        favorite_content_types = request.POST.getlist('favorite_content_types')
        profile.favorite_content_types = ','.join(favorite_content_types)
        profile.save()
        
        # Actualizar géneros favoritos
        favorite_genres = request.POST.getlist('favorite_genres')
        profile.favorite_genres.set(favorite_genres)
        
        messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('user_profile')
    
    genres = Genre.objects.all()
    content_types = ContentItem.CONTENT_TYPES
    
    context = {
        'profile': profile,
        'genres': genres,
        'content_types': content_types,
    }
    return render(request, 'profile.html', context)

@login_required
def test_apis(request):
    """Vista de prueba para las APIs externas"""
    if request.method == 'POST':
        query = request.POST.get('query', 'naruto')
        content_type = request.POST.get('content_type', '')
        
        try:
            results = search_content_from_apis(query, content_type, 5)
            return JsonResponse({
                'success': True,
                'results': results,
                'count': len(results)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return render(request, 'test_apis.html')

@login_required
def import_external_content(request):
    """Importar contenido desde APIs externas"""
    if request.method == 'POST':
        try:
            # Obtener datos del contenido desde la API
            api_data = json.loads(request.POST.get('api_data'))
            
            # Importar a la base de datos
            content = import_content_to_database(api_data)
            
            if content:
                messages.success(request, f'Contenido "{content.title}" importado exitosamente!')
                return JsonResponse({
                    'success': True, 
                    'message': 'Contenido importado exitosamente',
                    'content_id': content.id
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Error al importar el contenido'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    return redirect('login')