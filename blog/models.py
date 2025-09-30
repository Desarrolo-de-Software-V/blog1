from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
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
        super().save(*args, **kwargs)
        
        # Redimensionar imágenes
        if self.featured_image:
            self.resize_image(self.featured_image.path, (800, 600))
        if self.poster_image:
            self.resize_image(self.poster_image.path, (400, 600))
    
    def resize_image(self, image_path, size):
        """Redimensiona las imágenes para optimizar el rendimiento"""
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                img.save(image_path, optimize=True, quality=85)
    
    @property
    def rating_stars(self):
        return "⭐" * self.rating + "☆" * (5 - self.rating)

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