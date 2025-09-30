from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Subcategory, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'subcategory_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    def post_count(self, obj):
        count = obj.posts.filter(published=True).count()
        url = reverse('admin:blog_post_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} reseñas</a>', url, count)
    post_count.short_description = 'Reseñas publicadas'
    
    def subcategory_count(self, obj):
        count = obj.subcategories.count()
        if count > 0:
            url = reverse('admin:blog_subcategory_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} subcategorías</a>', url, count)
        return '0 subcategorías'
    subcategory_count.short_description = 'Subcategorías'

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'post_count', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['category__name', 'name']
    
    def post_count(self, obj):
        count = obj.posts.filter(published=True).count()
        url = reverse('admin:blog_post_changelist') + f'?subcategory__id__exact={obj.id}'
        return format_html('<a href="{}">{} reseñas</a>', url, count)
    post_count.short_description = 'Reseñas publicadas'

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['author', 'content', 'created_at', 'approved']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'movie_title', 'author', 'category', 'rating_display', 
        'published', 'featured', 'created_at', 'comment_count'
    ]
    list_filter = [
        'published', 'featured', 'category', 'subcategory', 'rating', 
        'created_at', 'release_year'
    ]
    search_fields = [
        'title', 'movie_title', 'director', 'content', 
        'author__username', 'author__first_name', 'author__last_name'
    ]
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'author', 'excerpt')
        }),
        ('Información de la Película/Anime', {
            'fields': ('movie_title', 'director', 'release_year', 'rating')
        }),
        ('Categorización', {
            'fields': ('category', 'subcategory')
        }),
        ('Contenido', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('Imágenes', {
            'fields': ('featured_image', 'poster_image'),
            'classes': ('collapse',)
        }),
        ('SEO y Metadatos', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Configuración de Publicación', {
            'fields': ('published', 'featured'),
            'classes': ('wide',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    inlines = [CommentInline]
    
    actions = ['make_published', 'make_unpublished', 'make_featured', 'remove_featured']
    
    def rating_display(self, obj):
        stars = "⭐" * obj.rating + "☆" * (5 - obj.rating)
        return format_html('<span title="{}/5 estrellas">{}</span>', obj.rating, stars)
    rating_display.short_description = 'Puntuación'
    
    def comment_count(self, obj):
        count = obj.comments.filter(approved=True).count()
        if count > 0:
            url = reverse('admin:blog_comment_changelist') + f'?post__id__exact={obj.id}'
            return format_html('<a href="{}">{} comentarios</a>', url, count)
        return '0 comentarios'
    comment_count.short_description = 'Comentarios'
    
    def make_published(self, request, queryset):
        count = queryset.update(published=True)
        self.message_user(request, f'{count} reseñas han sido publicadas.')
    make_published.short_description = 'Publicar reseñas seleccionadas'
    
    def make_unpublished(self, request, queryset):
        count = queryset.update(published=False)
        self.message_user(request, f'{count} reseñas han sido despublicadas.')
    make_unpublished.short_description = 'Despublicar reseñas seleccionadas'
    
    def make_featured(self, request, queryset):
        count = queryset.update(featured=True)
        self.message_user(request, f'{count} reseñas han sido destacadas.')
    make_featured.short_description = 'Destacar reseñas seleccionadas'
    
    def remove_featured(self, request, queryset):
        count = queryset.update(featured=False)
        self.message_user(request, f'{count} reseñas ya no son destacadas.')
    remove_featured.short_description = 'Quitar destaque de reseñas seleccionadas'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'author', 'category', 'subcategory'
        ).prefetch_related('comments')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'author', 'post_title', 'content_preview', 'created_at', 
        'approved', 'is_reply_display'
    ]
    list_filter = ['approved', 'created_at', 'post__category']
    search_fields = [
        'content', 'author__username', 'author__first_name', 
        'author__last_name', 'post__title'
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    actions = ['approve_comments', 'unapprove_comments']
    
    def post_title(self, obj):
        url = reverse('admin:blog_post_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title[:50])
    post_title.short_description = 'Reseña'
    
    def content_preview(self, obj):
        preview = obj.content[:100]
        if len(obj.content) > 100:
            preview += '...'
        return preview
    content_preview.short_description = 'Comentario'
    
    def is_reply_display(self, obj):
        if obj.is_reply:
            return format_html('<span style="color: #e74c3c;">🔗 Respuesta</span>')
        return format_html('<span style="color: #2c3e50;">💬 Principal</span>')
    is_reply_display.short_description = 'Tipo'
    
    def approve_comments(self, request, queryset):
        count = queryset.update(approved=True)
        self.message_user(request, f'{count} comentarios han sido aprobados.')
    approve_comments.short_description = 'Aprobar comentarios seleccionados'
    
    def unapprove_comments(self, request, queryset):
        count = queryset.update(approved=False)
        self.message_user(request, f'{count} comentarios han sido desaprobados.')
    unapprove_comments.short_description = 'Desaprobar comentarios seleccionados'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post', 'parent')

# Personalización del sitio de administración
admin.site.site_header = "MovieReviews - Administración"
admin.site.site_title = "MovieReviews Admin"
admin.site.index_title = "Panel de Administración"

# Registrar modelos adicionales si es necesario
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Extender el admin de usuarios para mostrar información adicional
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('post_count', 'comment_count', 'date_joined')
    
    def post_count(self, obj):
        count = obj.blog_posts.filter(published=True).count()
        if count > 0:
            url = reverse('admin:blog_post_changelist') + f'?author__id__exact={obj.id}'
            return format_html('<a href="{}">{} reseñas</a>', url, count)
        return '0 reseñas'
    post_count.short_description = 'Reseñas publicadas'
    
    def comment_count(self, obj):
        count = obj.comment_set.filter(approved=True).count()
        if count > 0:
            url = reverse('admin:blog_comment_changelist') + f'?author__id__exact={obj.id}'
            return format_html('<a href="{}">{} comentarios</a>', url, count)
        return '0 comentarios'
    comment_count.short_description = 'Comentarios aprobados'

# Re-registrar el modelo User con nuestro admin personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)