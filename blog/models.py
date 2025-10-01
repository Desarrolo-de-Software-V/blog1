from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from PIL import Image
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Subcategories"
        unique_together = ('category', 'slug')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('blog:subcategory_posts', kwargs={
            'category_slug': self.category.slug,
            'subcategory_slug': self.slug
        })

class Post(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, help_text="Breve descripción de la reseña")
    
    # Campos específicos para reseñas
    movie_title = models.CharField(max_length=200, verbose_name="Título de la película/anime")
    director = models.CharField(max_length=200, blank=True)
    release_year = models.IntegerField(help_text="Año de estreno")
    rating = models.IntegerField(choices=RATING_CHOICES, default=3)
    
    # Imágenes
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    poster_image = models.ImageField(upload_to='blog/posters/', blank=True, null=True, help_text="Poster de la película")
    
    # Metadatos
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False, help_text="Destacar en página principal")
    
    # Campos para SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['published', '-created_at']),
            models.Index(fields=['category', 'published']),
            models.Index(fields=['featured', 'published']),
        ]
    
    def __str__(self):
        return f"Reseña: {self.movie_title} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Generar slug automáticamente si no existe o si es un nuevo post
        if not self.slug or self.pk is None:
            self.slug = self.generate_unique_slug()
        
        super().save(*args, **kwargs)
        
        # Redimensionar imágenes
        if self.featured_image:
            self.resize_image(self.featured_image.path, (800, 600))
        if self.poster_image:
            self.resize_image(self.poster_image.path, (400, 600))
    
    def generate_unique_slug(self):
        """Genera un slug único basado en el título de la película"""
        from django.utils.text import slugify
        
        # Usar el título de la película como base para el slug
        base_slug = slugify(self.movie_title)
        slug = base_slug
        
        # Si el slug está vacío, usar el título del post
        if not slug:
            slug = slugify(self.title)
        
        # Verificar si el slug ya existe y agregar un número si es necesario
        counter = 1
        original_slug = slug
        while Post.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        return slug
    
    def resize_image(self, image_path, size):
        """Redimensiona las imágenes para optimizar el rendimiento"""
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                img.save(image_path, optimize=True, quality=85)
    
    @property
    def rating_stars(self):
        return "⭐" * self.rating + "☆" * (5 - self.rating)
    
    def get_reactions_count(self):
        """Retorna el número total de reacciones de la reseña"""
        return self.reactions.count()
    
    def get_reactions_by_type(self):
        """Retorna un diccionario con el conteo de cada tipo de reacción"""
        from django.db.models import Count
        return dict(self.reactions.values('reaction_type').annotate(count=Count('reaction_type')).values_list('reaction_type', 'count'))
    
    def get_user_reaction(self, user):
        """Retorna la reacción del usuario específico a esta reseña"""
        if not user.is_authenticated:
            return None
        try:
            return self.reactions.get(user=user).reaction_type
        except PostReaction.DoesNotExist:
            return None
    
    def has_user_reacted(self, user):
        """Verifica si un usuario específico ha reaccionado a esta reseña"""
        if not user.is_authenticated:
            return False
        return self.reactions.filter(user=user).exists()
    
    # Métodos de compatibilidad con el sistema anterior
    def get_likes_count(self):
        """Retorna el número total de likes (compatibilidad)"""
        return self.reactions.filter(reaction_type='like').count()
    
    def is_liked_by_user(self, user):
        """Verifica si un usuario específico ha dado like (compatibilidad)"""
        if not user.is_authenticated:
            return False
        return self.reactions.filter(user=user, reaction_type='like').exists()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comentario de {self.author.username} en {self.post.title}"
    
    @property
    def is_reply(self):
        return self.parent is not None
    
    def get_vote_score(self):
        """Retorna el puntaje total de votos del comentario"""
        upvotes = self.votes.filter(vote_type='upvote').count()
        downvotes = self.votes.filter(vote_type='downvote').count()
        return upvotes - downvotes
    
    def get_upvotes_count(self):
        """Retorna el número de upvotes"""
        return self.votes.filter(vote_type='upvote').count()
    
    def get_downvotes_count(self):
        """Retorna el número de downvotes"""
        return self.votes.filter(vote_type='downvote').count()
    
    def get_user_vote(self, user):
        """Retorna el voto del usuario específico"""
        if not user.is_authenticated:
            return None
        try:
            return self.votes.get(user=user).vote_type
        except CommentVote.DoesNotExist:
            return None
    
    def has_user_voted(self, user):
        """Verifica si el usuario ha votado en este comentario"""
        if not user.is_authenticated:
            return False
        return self.votes.filter(user=user).exists()
    
    def detect_mentions(self):
        """Detecta menciones (@usuario) en el contenido del comentario"""
        import re
        from django.contrib.auth.models import User
        
        # Patrón para detectar @usuario
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, self.content)
        
        mentioned_users = []
        for username in mentions:
            try:
                user = User.objects.get(username=username)
                if user != self.author:  # No mencionarse a sí mismo
                    mentioned_users.append(user)
            except User.DoesNotExist:
                # Usuario no existe, ignorar
                pass
        
        return mentioned_users
    
    def process_mentions(self):
        """Procesa las menciones y crea notificaciones"""
        mentioned_users = self.detect_mentions()
        
        for user in mentioned_users:
            # Crear notificación usando get_model para evitar importación circular
            from django.apps import apps
            Notification = apps.get_model('blog', 'Notification')
            Mention = apps.get_model('blog', 'Mention')
            
            Notification.objects.create(
                recipient=user,
                sender=self.author,
                notification_type='mention',
                title=f'{self.author.get_full_name() or self.author.username} te mencionó',
                message=f'Te mencionó en un comentario: "{self.content[:100]}..."',
                post=self.post,
                comment=self
            )
            
            # Crear registro de mención
            Mention.objects.get_or_create(
                comment=self,
                mentioned_user=user
            )

class CommentVote(models.Model):
    """Modelo para manejar votos de comentarios"""
    VOTE_TYPES = [
        ('upvote', '⬆️ Upvote'),
        ('downvote', '⬇️ Downvote'),
    ]
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_votes')
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('comment', 'user')  # Un usuario solo puede votar una vez por comentario
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} votó {self.get_vote_type_display()} en comentario de {self.comment.author.username}"

class PostReaction(models.Model):
    """Modelo para manejar reacciones de reseñas"""
    REACTION_TYPES = [
        ('like', '👍 Me gusta'),
        ('love', '❤️ Me encanta'),
        ('laugh', '😂 Me divierte'),
        ('wow', '😮 Me asombra'),
        ('sad', '😢 Me entristece'),
        ('angry', '😡 Me enoja'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')  # Un usuario solo puede tener una reacción por post
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} reaccionó con {self.get_reaction_type_display()} a {self.post.title}"

class Notification(models.Model):
    """Modelo para notificaciones del sistema"""
    NOTIFICATION_TYPES = [
        ('mention', 'Mencionado'),
        ('like', 'Me gusta'),
        ('comment', 'Comentario'),
        ('reply', 'Respuesta'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}: {self.title}"
    
    @property
    def get_absolute_url(self):
        """Devuelve la URL a la que debe dirigir la notificación"""
        if self.post:
            return self.post.get_absolute_url()
        elif self.comment and self.comment.post:
            return self.comment.post.get_absolute_url()
        return '#'

class Mention(models.Model):
    """Modelo para rastrear menciones de usuarios"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='mentions')
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('comment', 'mentioned_user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.comment.author.username} mencionó a {self.mentioned_user.username}"

class Subscription(models.Model):
    """Modelo para suscripciones de usuarios a autores o categorías"""
    SUBSCRIPTION_TYPES = [
        ('author', 'Autor'),
        ('category', 'Categoría'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPES)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscribers', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = [
            ('user', 'subscription_type', 'author'),
            ('user', 'subscription_type', 'category'),
        ]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['subscription_type', 'is_active']),
        ]
    
    def __str__(self):
        if self.subscription_type == 'author' and self.author:
            return f"{self.user.username} suscrito a {self.author.username}"
        elif self.subscription_type == 'category' and self.category:
            return f"{self.user.username} suscrito a {self.category.name}"
        return f"Suscripción de {self.user.username}"
    
    def clean(self):
        """Validar que solo se especifique autor o categoría según el tipo"""
        if self.subscription_type == 'author' and not self.author:
            raise ValidationError('Debe especificar un autor para suscripciones de tipo autor')
        if self.subscription_type == 'category' and not self.category:
            raise ValidationError('Debe especificar una categoría para suscripciones de tipo categoría')
        if self.subscription_type == 'author' and self.category:
            raise ValidationError('No puede especificar categoría para suscripciones de tipo autor')
        if self.subscription_type == 'category' and self.author:
            raise ValidationError('No puede especificar autor para suscripciones de tipo categoría')
