from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.urls import reverse
import re

register = template.Library()

@register.filter
def highlight(text, search_term):
    """
    Resalta los términos de búsqueda en el texto
    """
    if not search_term or not text:
        return text
    
    # Escapar HTML para seguridad
    escaped_text = escape(str(text))
    escaped_search = escape(str(search_term))
    
    # Crear patrón de búsqueda case-insensitive
    pattern = re.compile(re.escape(escaped_search), re.IGNORECASE)
    
    # Reemplazar con versión resaltada
    highlighted = pattern.sub(
        f'<mark class="highlight">{escaped_search}</mark>', 
        escaped_text
    )
    
    return mark_safe(highlighted)

@register.filter
def rating_percentage(rating):
    """
    Convierte una calificación de 1-5 a porcentaje
    """
    try:
        return int((float(rating) / 5.0) * 100)
    except (ValueError, TypeError):
        return 0

@register.filter
def rating_color(rating):
    """
    Devuelve una clase CSS basada en la calificación
    """
    try:
        rating = int(rating)
        if rating >= 4:
            return 'text-success'
        elif rating >= 3:
            return 'text-warning'
        else:
            return 'text-danger'
    except (ValueError, TypeError):
        return 'text-muted'

@register.filter
def truncate_smart(text, length=100):
    """
    Trunca texto de manera inteligente, evitando cortar palabras
    """
    if not text or len(text) <= length:
        return text
    
    truncated = text[:length]
    # Encontrar el último espacio
    last_space = truncated.rfind(' ')
    
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return f"{truncated}..."

@register.filter
def reading_time(text):
    """
    Calcula el tiempo estimado de lectura (250 palabras por minuto)
    """
    if not text:
        return 0
    
    word_count = len(text.split())
    minutes = max(1, round(word_count / 250))
    
    if minutes == 1:
        return "1 min de lectura"
    else:
        return f"{minutes} min de lectura"

@register.filter
def format_number(value):
    """
    Formatea números grandes de manera legible
    """
    try:
        num = int(value)
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        else:
            return str(num)
    except (ValueError, TypeError):
        return value

@register.simple_tag
def get_random_posts(count=3, exclude_id=None):
    """
    Obtiene posts aleatorios para sugerencias
    """
    from blog.models import Post
    
    posts = Post.objects.filter(published=True)
    if exclude_id:
        posts = posts.exclude(id=exclude_id)
    
    return posts.order_by('?')[:count]

@register.simple_tag
def get_popular_categories():
    """
    Obtiene las categorías más populares
    """
    from blog.models import Category
    from django.db.models import Count
    
    return Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__published=True))
    ).filter(post_count__gt=0).order_by('-post_count')[:5]

@register.simple_tag
def get_recent_comments(count=5):
    """
    Obtiene comentarios recientes
    """
    from blog.models import Comment
    
    return Comment.objects.filter(
        approved=True,
        post__published=True
    ).select_related('author', 'post').order_by('-created_at')[:count]

@register.inclusion_tag('blog/components/rating_stars.html')
def rating_stars(rating, show_text=True):
    """
    Template tag para mostrar estrellas de calificación
    """
    try:
        rating = int(rating)
    except (ValueError, TypeError):
        rating = 0
    
    return {
        'rating': rating,
        'stars_filled': range(rating),
        'stars_empty': range(5 - rating),
        'show_text': show_text
    }

@register.inclusion_tag('blog/components/breadcrumb.html')
def breadcrumb(items):
    """
    Template tag para breadcrumbs
    """
    return {'items': items}

@register.inclusion_tag('blog/components/social_share.html')
def social_share(post, request):
    """
    Template tag para botones de compartir en redes sociales
    """
    if request:
        current_url = request.build_absolute_uri()
    else:
        current_url = ""
    
    return {
        'post': post,
        'current_url': current_url,
        'twitter_text': f"Reseña: {post.title} - {post.movie_title}",
        'facebook_text': f"Te recomiendo esta reseña de {post.movie_title}"
    }

@register.filter
def add_class(field, css_class):
    """
    Añade clases CSS a campos de formulario
    """
    return field.as_widget(attrs={'class': css_class})

@register.filter
def multiply(value, factor):
    """
    Multiplica un valor por un factor
    """
    try:
        return float(value) * float(factor)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_item(dictionary, key):
    """
    Obtiene un item de un diccionario usando una key dinámica
    """
    return dictionary.get(key)

@register.simple_tag
def url_replace(request, field, value):
    """
    Reemplaza o añade un parámetro GET en la URL actual
    """
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.filter
def duration_humanize(duration):
    """
    Convierte duración en minutos a formato legible
    """
    try:
        minutes = int(duration)
        hours = minutes // 60
        remaining_minutes = minutes % 60
        
        if hours > 0:
            if remaining_minutes > 0:
                return f"{hours}h {remaining_minutes}m"
            else:
                return f"{hours}h"
        else:
            return f"{minutes}m"
    except (ValueError, TypeError):
        return duration

@register.filter
def category_icon(category_name):
    """
    Devuelve el icono FontAwesome apropiado para una categoría
    """
    category_lower = category_name.lower()
    
    if 'anime' in category_lower:
        return 'fas fa-dragon'
    elif 'película' in category_lower or 'movie' in category_lower:
        return 'fas fa-film'
    elif 'serie' in category_lower:
        return 'fas fa-tv'
    elif 'documental' in category_lower:
        return 'fas fa-book-open'
    else:
        return 'fas fa-folder-open'

@register.filter
def category_color(category_name):
    """
    Devuelve el color apropiado para una categoría
    """
    category_lower = category_name.lower()
    
    if 'anime' in category_lower:
        return 'warning'
    elif 'película' in category_lower or 'movie' in category_lower:
        return 'primary'
    elif 'serie' in category_lower:
        return 'info'
    elif 'documental' in category_lower:
        return 'success'
    else:
        return 'secondary'

from django.db.models import Q